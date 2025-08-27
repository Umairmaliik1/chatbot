import json
from datetime import datetime, timedelta
from typing import Union, Optional, List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import auth, models
from ..database import get_db

router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"]
)

def _get_date_range(period: str):
    """Calculates start and end dates based on a period string."""
    end_date = datetime.utcnow()
    if period == "7d":
        start_date = end_date - timedelta(days=7)
    elif period == "30d":
        start_date = end_date - timedelta(days=30)
    elif period == "90d":
        start_date = end_date - timedelta(days=90)
    else:
        raise HTTPException(status_code=400, detail="Invalid period specified.")
    return start_date, end_date

def _apply_filters(rows: List, filters_json: Optional[str]) -> List:
    """Applies filters to a list of rows."""
    if not filters_json:
        return rows
    try:
        filters = json.loads(filters_json)
        # Example filter logic (can be expanded)
        if "min_messages" in filters:
            rows = [row for row in rows if row['message_count'] >= filters["min_messages"]]
        return rows
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in filters.")

@router.get("/chat_sessions")
async def get_chat_session_report(
    request: Request,
    period: str = "30d",
    _: models.User = Depends(auth.get_current_user_for_api),
    db: Session = Depends(get_db)
):
    """
    Provides a report on chat session activity over a given period.
    """
    start_date, end_date = _get_date_range(period)
    
    query = (
        db.query(
            models.ChatSession.id,
            models.ChatSession.title,
            models.ChatSession.created_at,
            func.count(models.ChatMessage.id).label("message_count")
        )
        .join(models.ChatMessage, models.ChatSession.id == models.ChatMessage.session_id)
        .filter(models.ChatSession.created_at.between(start_date, end_date))
        .group_by(models.ChatSession.id)
        .order_by(models.ChatSession.created_at.desc())
    )
    
    results = query.all()

    # Convert SQLAlchemy results to a list of dictionaries
    report_data = [
        {
            "session_id": row.id,
            "title": row.title,
            "created_at": row.created_at.isoformat(),
            "message_count": row.message_count,
        }
        for row in results
    ]

    return report_data