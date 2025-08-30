"""
Unified AI client that supports both Gemini and OpenAI providers.
"""
import os
import logging
import asyncio
from typing import Iterator, List, Dict, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from .settings import settings

class UnifiedAIClient:
    """Unified AI client supporting both Gemini and OpenAI providers."""
    
    def __init__(self):
        """Initialize the unified AI client."""
        self.session_memories = {}  # session_id -> ConversationBufferMemory
        self.gemini_client = None
        self.openai_client = None
        
        # Initialize Gemini client if API key is available
        if settings.gemini_api_key:
            try:
                self.gemini_client = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    google_api_key=settings.gemini_api_key,
                    temperature=settings.temperature,
                    max_output_tokens=settings.max_tokens,
                    convert_system_message_to_human=True,
                    verbose=False
                )
                logging.info("Gemini client initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize Gemini client: {e}")
        
        # Initialize OpenAI client if API key is available
        if settings.openai_api_key:
            try:
                self.openai_client = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    openai_api_key=settings.openai_api_key,
                    temperature=settings.temperature,
                    max_tokens=settings.max_tokens,
                    verbose=False
                )
                logging.info("OpenAI client initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize OpenAI client: {e}")
    
    def _get_client_for_provider(self, provider: str):
        """Get the appropriate client for the specified provider."""
        if provider == "openai":
            if not self.openai_client:
                raise ValueError("OpenAI client not initialized. Please check OPENAI_API_KEY environment variable.")
            return self.openai_client
        elif provider == "gemini":
            if not self.gemini_client:
                raise ValueError("Gemini client not initialized. Please check GEMINI_API_KEY environment variable.")
            return self.gemini_client
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
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
    
    def _prepare_messages(self, history: List[Dict], system_prompt: str, provider: str) -> List:
        """Prepare messages for the AI model based on provider requirements."""
        messages = []
        
        # Add system message (OpenAI supports it directly, Gemini converts to human)
        if system_prompt:
            if provider == "openai":
                messages.append(SystemMessage(content=system_prompt))
            else:  # Gemini
                # For Gemini, we'll prepend the system message to the first user message
                if history and history[0]["role"] == "user":
                    history[0]["content"] = f"{system_prompt}\n\nUser: {history[0]['content']}"
                else:
                    messages.append(HumanMessage(content=system_prompt))
        
        # Add conversation history
        for msg in history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        
        return messages
    
    def generate_stream(
        self, 
        history: List[Dict], 
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        system_prompt: str = "",
        user_id: Optional[int] = None,
        db_session=None,
        session_id: Optional[int] = None,
        provider: str = "gemini"
    ) -> Iterator[str]:
        """
        Generate streaming response using the specified provider.
        """
        try:
            # Get the appropriate client
            client = self._get_client_for_provider(provider)
            
            # Update client parameters if provided
            if max_tokens:
                if provider == "openai":
                    client.max_tokens = max_tokens
                else:  # Gemini
                    client.max_output_tokens = max_tokens
            
            if temperature is not None:
                client.temperature = temperature
            
            # Prepare messages
            messages = self._prepare_messages(history, system_prompt, provider)
            
            # Get the last user message for memory
            last_user_message = ""
            if history and history[-1]["role"] == "user":
                last_user_message = history[-1]["content"]
            
            # Stream the response
            full_response = ""
            
            # Use streaming if available
            try:
                for chunk in client.stream(messages):
                    if hasattr(chunk, 'content') and chunk.content:
                        content = chunk.content
                        full_response += content
                        yield content
            except Exception as stream_error:
                logging.warning(f"Streaming failed for {provider}, falling back to regular generation: {stream_error}")
                # Fallback to regular generation
                response = client.invoke(messages)
                content = response.content if hasattr(response, 'content') else str(response)
                full_response = content
                # Simulate streaming by yielding character by character
                for char in content:
                    yield char
                    # Small delay to simulate streaming
                    import time
                    time.sleep(0.01)
            
            # Add to memory if session_id is provided
            if session_id and last_user_message:
                self._add_to_memory(session_id, last_user_message, full_response)
            
        except Exception as e:
            logging.error(f"Error in generate_stream with {provider}: {e}")
            error_message = f"I'm having trouble connecting to the {provider.upper()} service. Please try again later."
            yield error_message
    
    def clear_session_memory(self, session_id: int):
        """Clear conversation memory for a specific session."""
        if session_id in self.session_memories:
            del self.session_memories[session_id]
            logging.info(f"Cleared memory for session {session_id}")
    
    def get_session_memory_info(self, session_id: int) -> dict:
        """Get information about a session's memory."""
        if session_id not in self.session_memories:
            return {"message_count": 0, "memory_size": 0}
        
        memory = self.session_memories[session_id]
        messages = memory.chat_memory.messages
        
        return {
            "message_count": len(messages),
            "memory_size": len(str(messages)),
            "session_id": session_id
        }
    
    def is_provider_available(self, provider: str) -> bool:
        """Check if a provider is available."""
        if provider == "openai":
            return self.openai_client is not None
        elif provider == "gemini":
            return self.gemini_client is not None
        return False

# Global instance
ai_client = None

def get_ai_client() -> UnifiedAIClient:
    """Get or create the global AI client instance."""
    global ai_client
    if ai_client is None:
        ai_client = UnifiedAIClient()
    return ai_client
