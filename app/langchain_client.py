"""
LangChain-based client for Gemini API integration.
Provides robust error handling, better context management, and conversation memory.
"""
import os
import logging
from typing import Iterator, List, Dict, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

class LangChainGeminiClient:
    """LangChain-based client for Gemini API with robust error handling and conversation memory."""
    
    def __init__(self):
        """Initialize the LangChain Gemini client."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Initialize the LangChain Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=self.api_key,
            temperature=0.7,
            max_output_tokens=512,
            convert_system_message_to_human=True,  # Gemini doesn't support system messages directly
            verbose=False
        )
        
        # Initialize conversation memory for each session
        self.session_memories = {}  # session_id -> ConversationBufferMemory
        
        logging.info("LangChain Gemini client initialized successfully")
    
    def _get_or_create_memory(self, session_id: int) -> ConversationBufferMemory:
        """Get or create conversation memory for a specific session."""
        if session_id not in self.session_memories:
            self.session_memories[session_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="output"
            )
        return self.session_memories[session_id]
    
    def _add_to_memory(self, session_id: int, user_message: str, assistant_message: str):
        """Add a conversation turn to the session memory."""
        memory = self._get_or_create_memory(session_id)
        memory.chat_memory.add_user_message(user_message)
        memory.chat_memory.add_ai_message(assistant_message)
    
    def _get_conversation_history(self, session_id: int) -> List:
        """Get conversation history for a specific session."""
        memory = self._get_or_create_memory(session_id)
        return memory.chat_memory.messages
    
    def clear_session_memory(self, session_id: int):
        """Clear conversation memory for a specific session."""
        if session_id in self.session_memories:
            del self.session_memories[session_id]
            logging.info(f"Cleared memory for session {session_id}")
    
    def generate_stream(self, messages: List[Dict], max_tokens: int = 512, 
                       temperature: float = 0.7, system_prompt: str = None, 
                       user_id: int = None, db_session = None, session_id: int = None) -> Iterator[str]:
        """
        Generate streaming response using LangChain with robust error handling and conversation memory.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            max_tokens: Maximum tokens for response
            temperature: Response creativity (0.0 to 1.0)
            system_prompt: System instructions (if any)
            user_id: User ID for context
            db_session: Database session for fetching user context
            session_id: Chat session ID for conversation memory
            
        Yields:
            Response text chunks
        """
        try:
            # Build context from instructions and FAQs
            context_parts = []
            
            # Add system prompt if provided
            if system_prompt:
                context_parts.append(f"INSTRUCTIONS:\n{system_prompt}")
            
            # Add user instructions and FAQs if available
            if user_id and db_session:
                try:
                    from .routers.instructions_api import get_relevant_faqs
                    
                    # Get user instructions using user_id (not user object)
                    user_instruction = db_session.query(models.UserInstruction).filter(
                        models.UserInstruction.user_id == user_id
                    ).first()
                    
                    if user_instruction:
                        context_parts.append(f"INSTRUCTIONS:\n{user_instruction.instructions}")
                        logging.info(f"✅ Added user instructions to context")
                    
                    # Get relevant FAQs based on last user message
                    if messages:
                        last_user_message = messages[-1]['content'] if messages[-1]['role'] == 'user' else ""
                        if last_user_message:
                            faq_context = get_relevant_faqs(user_id, last_user_message, db_session)
                            if faq_context:
                                context_parts.append(faq_context)
                                logging.info(f"✅ Added FAQ context to context")
                                
                except Exception as e:
                    logging.warning(f"Could not load user context: {e}")
                    logging.warning(f"User ID: {user_id}, DB Session: {db_session}")
            
            # Build final context
            final_context = "\n\n".join(context_parts) if context_parts else ""
            logging.info(f"🔧 Final context built: {len(context_parts)} parts, total length: {len(final_context)}")
            
            # Get current user message (last message should be from user)
            current_user_message = ""
            if messages and messages[-1]['role'] == 'user':
                current_user_message = messages[-1]['content']
                logging.info(f"📝 Current user message: {current_user_message[:100]}...")
            else:
                logging.warning(f"⚠️ No user message found in messages: {messages}")
            
            # Prepare messages for LangChain with conversation memory
            langchain_messages = []
            
            # Add system context if available
            if final_context:
                langchain_messages.append(
                    HumanMessage(content=f"{final_context}\n\nYou are a helpful AI assistant. Use the context above to provide accurate responses.")
                )
                logging.info(f"✅ Added system context message")
            
            # Add conversation history from memory if available
            if session_id:
                conversation_history = self._get_conversation_history(session_id)
                if conversation_history:
                    # Add previous conversation turns
                    langchain_messages.extend(conversation_history)
                    logging.info(f"✅ Added {len(conversation_history)} previous messages to context for session {session_id}")
                else:
                    logging.info(f"ℹ️ No conversation history found for session {session_id}")
            
            # Add current user message
            if current_user_message:
                langchain_messages.append(HumanMessage(content=current_user_message))
                logging.info(f"✅ Added current user message")
            else:
                logging.error(f"❌ No current user message to add")
            
            logging.info(f"📤 Final LangChain messages to send: {len(langchain_messages)}")
            for i, msg in enumerate(langchain_messages):
                logging.info(f"📤 Message {i}: {type(msg).__name__} - {msg.content[:200]}...")
            
            # Generate response using LangChain
            try:
                logging.info(f"🔄 Starting LangChain generation with {len(langchain_messages)} messages")
                logging.info(f"🔄 First message content: {langchain_messages[0].content[:100] if langchain_messages else 'No messages'}")
                
                # Use the LLM directly for generation
                response = self.llm.invoke(langchain_messages)
                logging.info(f"✅ LangChain response received: {type(response)}")
                
                if response and hasattr(response, 'content'):
                    response_text = response.content
                    logging.info(f"✅ Response content length: {len(response_text) if response_text else 0}")
                    
                    # Add to conversation memory if session_id is provided
                    if session_id and current_user_message and response_text:
                        self._add_to_memory(session_id, current_user_message, response_text)
                        logging.info(f"Added conversation turn to memory for session {session_id}")
                    
                    # Simulate streaming by yielding response in chunks
                    if response_text:
                        # Split response into words and yield in chunks
                        words = response_text.split()
                        chunk_size = max(1, len(words) // 10)  # 10 chunks
                        logging.info(f"📦 Streaming response in {chunk_size} word chunks, total words: {len(words)}")
                        
                        for i in range(0, len(words), chunk_size):
                            chunk = " ".join(words[i:i + chunk_size])
                            if chunk.strip():
                                yield chunk + " "
                    else:
                        logging.warning("⚠️ Empty response from LangChain")
                        yield "I apologize, but I couldn't generate a response. Please try again."
                        
                else:
                    logging.error(f"❌ Invalid response from LangChain: {response}")
                    yield "I apologize, but I couldn't generate a response. Please try again."
                    
            except Exception as e:
                logging.error(f"❌ Error in LangChain generation: {e}")
                logging.error(f"❌ Error type: {type(e)}")
                logging.error(f"❌ Error details: {str(e)}")
                import traceback
                logging.error(f"❌ Full traceback: {traceback.format_exc()}")
                
                # Check for specific Gemini errors
                error_str = str(e).lower()
                if "finish_reason" in error_str and ("1" in error_str or "2" in error_str):
                    yield "I apologize, but I cannot generate a response to this request due to content safety restrictions. Please try rephrasing your question or ask about a different topic."
                elif "quota" in error_str or "rate limit" in error_str:
                    yield "I'm experiencing high demand right now. Please try again in a moment."
                elif "invalid" in error_str or "malformed" in error_str:
                    yield "I encountered an issue processing your request. Please try rephrasing your question."
                else:
                    yield f"I'm having trouble generating a response right now. Error: {str(e)[:100]}"
                    
        except Exception as e:
            logging.error(f"Critical error in LangChain client: {e}")
            yield "I'm experiencing technical difficulties. Please try again later."
    
    def generate_response(self, messages: List[Dict], max_tokens: int = 512, 
                         temperature: float = 0.7, system_prompt: str = None, 
                         user_id: int = None, db_session = None, session_id: int = None) -> str:
        """
        Generate a single response (non-streaming) using LangChain.
        
        Args:
            messages: List of message dictionaries
            max_tokens: Maximum tokens for response
            temperature: Response creativity
            system_prompt: System instructions
            user_id: User ID for context
            db_session: Database session
            session_id: Chat session ID for conversation memory
            
        Returns:
            Generated response text
        """
        try:
            # Use the streaming method but collect all chunks
            response_chunks = list(self.generate_stream(
                messages, max_tokens, temperature, system_prompt, user_id, db_session, session_id
            ))
            return "".join(response_chunks).strip()
            
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return "I'm having trouble generating a response right now. Please try again."
    
    def get_session_memory_info(self, session_id: int) -> Dict:
        """Get information about a session's memory."""
        if session_id in self.session_memories:
            memory = self.session_memories[session_id]
            return {
                "session_id": session_id,
                "message_count": len(memory.chat_memory.messages),
                "has_memory": True
            }
        return {
            "session_id": session_id,
            "message_count": 0,
            "has_memory": False
        }
    
    def list_active_sessions(self) -> List[int]:
        """List all active session IDs with memory."""
        return list(self.session_memories.keys())

# Import models for type hints
try:
    from . import models
except ImportError:
    models = None
