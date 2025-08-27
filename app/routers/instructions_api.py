"""
API router for user instructions and FAQ management.
"""
import logging
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import re
import io

from .. import models, auth
from ..database import get_db
from ..schemas import (
    InstructionCreate, InstructionResponse,
    FAQCreate, FAQUpdate, FAQResponse
)

router = APIRouter()

@router.post("/instructions", response_model=InstructionResponse)
async def create_or_update_instructions(
    instruction_data: InstructionCreate,
    user: models.User = Depends(auth.get_current_user_for_api),
    db: Session = Depends(get_db)
):
    """Create or update user's system instructions."""
    try:
        # Check if instructions already exist
        existing_instruction = db.query(models.UserInstruction).filter(
            models.UserInstruction.user_id == user.id
        ).first()
        
        if existing_instruction:
            # Update existing
            existing_instruction.instructions = instruction_data.instructions
            db.commit()
            db.refresh(existing_instruction)
            return existing_instruction
        else:
            # Create new
            new_instruction = models.UserInstruction(
                user_id=user.id,
                instructions=instruction_data.instructions
            )
            db.add(new_instruction)
            db.commit()
            db.refresh(new_instruction)
            return new_instruction
            
    except Exception as e:
        db.rollback()
        logging.error(f"Error creating/updating instructions: {e}")
        raise HTTPException(status_code=500, detail="Failed to save instructions")

@router.get("/instructions", response_model=InstructionResponse)
async def get_instructions(
    user: models.User = Depends(auth.get_current_user_for_api),
    db: Session = Depends(get_db)
):
    """Get user's current system instructions."""
    instruction = db.query(models.UserInstruction).filter(
        models.UserInstruction.user_id == user.id
    ).first()
    
    if not instruction:
        raise HTTPException(status_code=404, detail="No instructions found")
    
    return instruction

@router.post("/parse-instructions-file")
async def parse_instructions_file(
    file: UploadFile = File(...),
    user: models.User = Depends(auth.get_current_user_for_api)
):
    """Parse uploaded file and extract text content for instructions."""
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.txt', '.pdf')):
            raise HTTPException(status_code=400, detail="Only .txt and .pdf files are supported")
        
        # Read file content
        content = await file.read()
        
        if file.filename.lower().endswith('.txt'):
            # Parse text file
            text_content = content.decode('utf-8')
        elif file.filename.lower().endswith('.pdf'):
            # Parse PDF file
            try:
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
                text_content = ""
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"
            except ImportError:
                # Fallback to pdfplumber if PyPDF2 is not available
                try:
                    import pdfplumber
                    with pdfplumber.open(io.BytesIO(content)) as pdf:
                        text_content = ""
                        for page in pdf.pages:
                            text_content += page.extract_text() + "\n"
                except ImportError:
                    raise HTTPException(
                        status_code=500, 
                        detail="PDF parsing requires PyPDF2 or pdfplumber. Please install one of these packages."
                    )
        
        # Clean up text content
        text_content = text_content.strip()
        if not text_content:
            raise HTTPException(status_code=400, detail="File appears to be empty or could not be parsed")
        
        return {"content": text_content}
        
    except Exception as e:
        logging.error(f"Error parsing instructions file: {e}")
        if "PDF parsing requires" in str(e):
            raise HTTPException(status_code=500, detail=str(e))
        raise HTTPException(status_code=500, detail="Failed to parse file")

@router.post("/faqs", response_model=FAQResponse)
async def create_faq(
    faq_data: FAQCreate,
    user: models.User = Depends(auth.get_current_user_for_api),
    db: Session = Depends(get_db)
):
    """Create a new FAQ."""
    try:
        new_faq = models.FAQ(
            user_id=user.id,
            question=faq_data.question,
            answer=faq_data.answer,
            priority=faq_data.priority or 1
        )
        db.add(new_faq)
        db.commit()
        db.refresh(new_faq)
        return new_faq
        
    except Exception as e:
        db.rollback()
        logging.error(f"Error creating FAQ: {e}")
        raise HTTPException(status_code=500, detail="Failed to create FAQ")

@router.get("/faqs", response_model=List[FAQResponse])
async def get_faqs(
    user: models.User = Depends(auth.get_current_user_for_api),
    db: Session = Depends(get_db)
):
    """Get all FAQs for the user."""
    faqs = db.query(models.FAQ).filter(
        models.FAQ.user_id == user.id
    ).order_by(models.FAQ.priority.desc(), models.FAQ.created_at.desc()).all()
    
    return faqs

@router.put("/faqs/{faq_id}", response_model=FAQResponse)
async def update_faq(
    faq_id: int,
    faq_data: FAQUpdate,
    user: models.User = Depends(auth.get_current_user_for_api),
    db: Session = Depends(get_db)
):
    """Update an existing FAQ."""
    faq = db.query(models.FAQ).filter(
        models.FAQ.id == faq_id,
        models.FAQ.user_id == user.id
    ).first()
    
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    
    try:
        if faq_data.question is not None:
            faq.question = faq_data.question
        if faq_data.answer is not None:
            faq.answer = faq_data.answer
        if faq_data.priority is not None:
            faq.priority = faq_data.priority
            
        db.commit()
        db.refresh(faq)
        return faq
        
    except Exception as e:
        db.rollback()
        logging.error(f"Error updating FAQ: {e}")
        raise HTTPException(status_code=500, detail="Failed to update FAQ")

@router.delete("/faqs/{faq_id}")
async def delete_faq(
    faq_id: int,
    user: models.User = Depends(auth.get_current_user_for_api),
    db: Session = Depends(get_db)
):
    """Delete an FAQ."""
    faq = db.query(models.FAQ).filter(
        models.FAQ.id == faq_id,
        models.FAQ.user_id == user.id
    ).first()
    
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    
    try:
        db.delete(faq)
        db.commit()
        return {"message": "FAQ deleted successfully"}
        
    except Exception as e:
        db.rollback()
        logging.error(f"Error deleting FAQ: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete FAQ")

@router.post("/parse-faq-file")
async def parse_faq_file(
    file: UploadFile = File(...),
    user: models.User = Depends(auth.get_current_user_for_api)
):
    """Parse uploaded file and extract FAQ content."""
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.txt', '.pdf')):
            raise HTTPException(status_code=400, detail="Only .txt and .pdf files are supported")
        
        # Read file content
        content = await file.read()
        
        if file.filename.lower().endswith('.txt'):
            # Parse text file
            text_content = content.decode('utf-8')
        elif file.filename.lower().endswith('.pdf'):
            # Parse PDF file
            try:
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
                text_content = ""
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"
            except ImportError:
                # Fallback to pdfplumber if PyPDF2 is not available
                try:
                    import pdfplumber
                    with pdfplumber.open(io.BytesIO(content)) as pdf:
                        text_content = ""
                        for page in pdf.pages:
                            text_content += page.extract_text() + "\n"
                except ImportError:
                    raise HTTPException(
                        status_code=500, 
                        detail="PDF parsing requires PyPDF2 or pdfplumber. Please install one of these packages."
                    )
        
        # Parse FAQ content
        faqs = parse_faq_text(text_content)
        
        if not faqs:
            raise HTTPException(status_code=400, detail="No valid FAQ format found in file. Expected format: Q: Question\nA: Answer")
        
        return {"faqs": faqs}
        
    except Exception as e:
        logging.error(f"Error parsing FAQ file: {e}")
        if "PDF parsing requires" in str(e):
            raise HTTPException(status_code=500, detail=str(e))
        raise HTTPException(status_code=500, detail="Failed to parse file")

def parse_faq_text(text: str) -> List[dict]:
    """
    Parse text content and extract FAQ pairs.
    Expected format: Q: Question\nA: Answer
    """
    faqs = []
    
    # Split by potential question markers
    lines = text.split('\n')
    current_question = None
    current_answer = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if line starts with question marker
        if line.upper().startswith(('Q:', 'QUESTION:', 'Q.', 'QUESTION.')):
            # Save previous FAQ if exists
            if current_question and current_answer:
                faqs.append({
                    "question": current_question,
                    "answer": " ".join(current_answer).strip(),
                    "priority": 1
                })
            
            # Start new FAQ
            current_question = line.split(':', 1)[1].strip() if ':' in line else line.split('.', 1)[1].strip()
            current_answer = []
            
        elif line.upper().startswith(('A:', 'ANSWER:', 'A.', 'ANSWER.')):
            # This is an answer line
            answer_text = line.split(':', 1)[1].strip() if ':' in line else line.split('.', 1)[1].strip()
            current_answer.append(answer_text)
            
        elif current_question and current_answer:
            # Continue building current answer
            current_answer.append(line)
    
    # Add the last FAQ if exists
    if current_question and current_answer:
        faqs.append({
            "question": current_question,
            "answer": " ".join(current_answer).strip(),
            "priority": 1
        })
    
    return faqs

def get_relevant_faqs(user_id: int, user_message: str, db: Session) -> str:
    """
    Get relevant FAQs based on simple keyword matching.
    Returns 70% of total FAQs, prioritizing by keyword matches.
    """
    try:
        # Get all FAQs for the user
        all_faqs = db.query(models.FAQ).filter(
            models.FAQ.user_id == user_id
        ).order_by(models.FAQ.priority.desc(), models.FAQ.created_at.desc()).all()
        
        if not all_faqs:
            return ""
        
        # Calculate how many FAQs to include (70% of total)
        faq_count = len(all_faqs)
        faqs_to_include = max(1, int(faq_count * 0.7))
        
        # Simple keyword matching
        user_words = set(re.findall(r'\b\w+\b', user_message.lower()))
        
        # Score FAQs based on keyword matches
        scored_faqs = []
        for faq in all_faqs:
            faq_words = set(re.findall(r'\b\w+\b', faq.question.lower()))
            matches = len(user_words.intersection(faq_words))
            score = matches + (faq.priority * 0.1)  # Include priority as tiebreaker
            scored_faqs.append((score, faq))
        
        # Sort by score and take top 70%
        scored_faqs.sort(key=lambda x: x[0], reverse=True)
        selected_faqs = scored_faqs[:faqs_to_include]
        
        # Build FAQ context string
        if not selected_faqs:
            return ""
        
        faq_context = "FAQS:\n"
        for _, faq in selected_faqs:
            faq_context += f"Q: {faq.question}\n"
            faq_context += f"A: {faq.answer}\n\n"
        
        return faq_context.strip()
        
    except Exception as e:
        logging.error(f"Error getting relevant FAQs: {e}")
        return ""
