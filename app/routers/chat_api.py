"""
Chat API router for handling chat functionality.
"""
import logging
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Dict
import json

from .. import models, auth
from ..database import get_db
from ..langchain_client import LangChainGeminiClient  # Updated import

router = APIRouter()

# Initialize LangChain Gemini client
try:
    gemini_client = LangChainGeminiClient()
    logging.info("✅ LangChain Gemini client initialized successfully")
except Exception as e:
    logging.error(f"❌ Failed to initialize LangChain Gemini client: {e}")
    gemini_client = None

@router.get("/test")
async def test_endpoint():
    """Simple test endpoint to verify API is accessible."""
    return {"message": "Chat API is working!", "status": "success"}

@router.post("/chat")
async def chat_endpoint(
    request: Request,
    user: models.User = Depends(auth.get_current_user_for_api),
    db: Session = Depends(get_db)
):
    """Chat endpoint that streams responses from Gemini API with conversation memory."""
    
    if not gemini_client:
        raise HTTPException(status_code=500, detail="AI service is not available")
    
    try:
        # Get request data
        data = await request.json()
        message = data.get("message", "").strip()
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Get chat session
        session_id = data.get("session_id")
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")
        
        # Capture the user ID early to avoid session binding issues
        user_id = user.id
        
        # Get or create chat session
        chat_session = db.query(models.ChatSession).filter(
            models.ChatSession.id == session_id,
            models.ChatSession.user_id == user_id  # Use captured user ID
        ).first()
        
        if not chat_session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Capture the session ID to avoid session binding issues
        chat_session_id = chat_session.id
        
        # Save user message
        user_message = models.ChatMessage(
            session_id=chat_session_id,
            role="user",
            content=message
        )
        db.add(user_message)
        db.commit()
        
        # Get user-specific instructions from the database
        instruction_entry = db.query(models.UserInstruction).filter(
            models.UserInstruction.user_id == user_id
        ).first()

        if instruction_entry and instruction_entry.instructions:
            instructions = instruction_entry.instructions
        else:
            logging.info("No user instructions found, using default prompt")
            instructions = "You are a helpful AI assistant."
        
        # Get chat history
        history = db.query(models.ChatMessage).filter(
            models.ChatMessage.session_id == chat_session_id
        ).order_by(models.ChatMessage.created_at.asc()).all()
        
        # Convert to format expected by Gemini client
        history_dicts = [
            {"role": msg.role, "content": msg.content}
            for msg in history
        ]
        
        # Create streaming response
        async def stream_and_save_logic():
            try:
                # Generate the response stream using LangChain client with session memory
                stream = gemini_client.generate_stream(
                    history_dicts, 
                    max_tokens=512, 
                    temperature=0.7, 
                    system_prompt=instructions,
                    user_id=user_id,  # Use captured user ID instead of user.id
                    db_session=db,
                    session_id=session_id  # Pass session_id for conversation memory
                )
                
                # Stream the response
                full_response = ""
                for chunk in stream:
                    full_response += chunk
                    yield f"data: {json.dumps({'content': chunk})}\n\n"
                
                # Save the complete response
                if full_response.strip():
                    assistant_message = models.ChatMessage(
                        session_id=chat_session_id,  # Use captured session ID
                        role="assistant",
                        content=full_response.strip()
                    )
                    db.add(assistant_message)
                    db.commit()
                
                # Send end signal
                yield f"data: {json.dumps({'content': '[DONE]'})}\n\n"
                
            except Exception as e:
                logging.error(f"Error in chat stream: {e}")
                error_message = "I'm having trouble responding right now. Please try again."
                yield f"data: {json.dumps({'content': error_message})}\n\n"
                yield f"data: {json.dumps({'content': '[DONE]'})}\n\n"
        
        return StreamingResponse(
            stream_and_save_logic(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
        
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/chat-history/{session_id}")
async def get_chat_history(
    session_id: int,
    user: models.User = Depends(auth.get_current_user_for_api),
    db: Session = Depends(get_db)
):
    """Get chat history for a specific session."""
    
    # Verify session belongs to user
    session = db.query(models.ChatSession).filter(
        models.ChatSession.id == session_id,
        models.ChatSession.user_id == user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    # Get messages
    messages = db.query(models.ChatMessage).filter(
        models.ChatMessage.session_id == session_id
    ).order_by(models.ChatMessage.created_at.asc()).all()
    
    return {
        "session_id": session_id,
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]
    }

@router.post("/chat-sessions")
async def create_chat_session(
    user: models.User = Depends(auth.get_current_user_for_api),
    db: Session = Depends(get_db)
):
    """Create a new chat session."""
    
    try:
        session = models.ChatSession(
            user_id=user.id,
            title="New Chat"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return {
            "session_id": session.id,
            "title": session.title,
            "created_at": session.created_at.isoformat()
        }
        
    except Exception as e:
        db.rollback()
        logging.error(f"Error creating chat session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create chat session")

@router.get("/chat-sessions")
async def get_user_chat_sessions(
    user: models.User = Depends(auth.get_current_user_for_api),
    db: Session = Depends(get_db)
):
    """Get all chat sessions for the current user."""
    
    sessions = db.query(models.ChatSession).filter(
        models.ChatSession.user_id == user.id
    ).order_by(models.ChatSession.updated_at.desc()).all()
    
    return [
        {
            "id": session.id,
            "title": session.title,
            "created_at": session.created_at.isoformat(),
            "updated_at": session.updated_at.isoformat()
        }
        for session in sessions
    ]

@router.delete("/chat-sessions/{session_id}")
async def delete_chat_session(
    session_id: int,
    user: models.User = Depends(auth.get_current_user_for_api),
    db: Session = Depends(get_db)
):
    """Delete a chat session and all its messages."""
    
    # Verify session belongs to user
    session = db.query(models.ChatSession).filter(
        models.ChatSession.id == session_id,
        models.ChatSession.user_id == user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    try:
        # Clear the session memory from LangChain client
        if gemini_client:
            gemini_client.clear_session_memory(session_id)
            logging.info(f"Cleared LangChain memory for session {session_id}")
        
        # Delete all messages first (cascade should handle this)
        db.delete(session)
        db.commit()
        
        return {"message": "Chat session deleted successfully"}
        
    except Exception as e:
        db.rollback()
        logging.error(f"Error deleting chat session: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete chat session")

@router.get("/chat-memory/{session_id}")
async def get_chat_memory_info(
    session_id: int,
    user: models.User = Depends(auth.get_current_user_for_api),
    db: Session = Depends(get_db)
):
    """Get information about a chat session's memory."""
    
    # Verify session belongs to user
    session = db.query(models.ChatSession).filter(
        models.ChatSession.id == session_id,
        models.ChatSession.user_id == user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    if not gemini_client:
        raise HTTPException(status_code=500, detail="AI service is not available")
    
    # Get memory information from LangChain client
    memory_info = gemini_client.get_session_memory_info(session_id)
    
    return memory_info

@router.delete("/chat-memory/{session_id}")
async def clear_chat_memory(
    session_id: int,
    user: models.User = Depends(auth.get_current_user_for_api),
    db: Session = Depends(get_db)
):
    """Clear conversation memory for a specific chat session."""
    
    # Verify session belongs to user
    session = db.query(models.ChatSession).filter(
        models.ChatSession.id == session_id,
        models.ChatSession.user_id == user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    if not gemini_client:
        raise HTTPException(status_code=500, detail="AI service is not available")
    
    try:
        # Clear the session memory from LangChain client
        gemini_client.clear_session_memory(session_id)
        
        return {"message": f"Conversation memory cleared for session {session_id}"}
        
    except Exception as e:
        logging.error(f"Error clearing chat memory: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear conversation memory")