# app/routers/kommo_api.py
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .. import models, auth
from ..database import get_db
from ..kommo_client import KommoClient
from ..kommo_webhooks import KommoWebhookHandler

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/kommo", tags=["Kommo"])

# -------------------------------
# Helpers
# -------------------------------
def _normalize_domain(raw: str) -> str:
    if not raw:
        return ""
    raw = raw.strip().replace("https://", "").replace("http://", "").rstrip("/")
    if "." not in raw:
        return f"{raw}.kommo.com"
    return raw

def _webhook_url(request: Request, integration_key: str) -> str:
    # Builds absolute webhook URL to show in UI
    return str(request.url_for("kommo_webhook", integration_key=integration_key))

# -------------------------------
# Schemas
# -------------------------------
class ConfigureJSON(BaseModel):
    # what your UI currently sends:
    api_key: Optional[str] = Field(None, description="long-lived token or access_token")
    subdomain: str = Field(..., description="e.g. theaiexpert735.kommo.com OR theaiexpert735")

    # optional extras (accepted if present)
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    webhook_secret: Optional[str] = None


class WidgetRequestPayload(BaseModel):
    message: str
    chat_id: str
    lead_id: Optional[str] = None
    visitor_id: Optional[str] = None
    from_: Optional[str] = Field(None, alias="from")

# -------------------------------
# Status
# -------------------------------
@router.get("/integration/status")
async def get_integration_status(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user_for_api),
):
    integ = db.query(models.KommoIntegration).filter(
        models.KommoIntegration.user_id == current_user.id
    ).first()

    if not integ:
        return {
            "active": False,
            "message": "No Kommo integration configured",
            "integration_key": current_user.kommo_integration_key,
            "webhook_url": _webhook_url(request, current_user.kommo_integration_key or "missing"),
        }

    return {
        "active": bool(integ.is_active),
        "kommo_domain": integ.kommo_domain,
        "last_sync": integ.last_sync_at,
        "integration_key": current_user.kommo_integration_key,
        "webhook_url": _webhook_url(request, current_user.kommo_integration_key),
        "created_at": integ.created_at,
        "updated_at": integ.updated_at,
    }

# Alias you asked for; /api/kommo/status → same as above
@router.get("/status")
async def get_integration_status_alias(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user_for_api),
):
    return await get_integration_status(request, db, current_user)

# -------------------------------
# Configure (JSON)  ← matches your UI call
# -------------------------------
@router.post("/configure")
async def configure_integration_json(
    payload: ConfigureJSON,
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user_for_api),
):
    """
    Accepts JSON:
    {
      "api_key": "<long-lived token OR access_token>",
      "subdomain": "theaiexpert735.kommo.com"
    }
    """
    domain = _normalize_domain(payload.subdomain)
    if not domain:
        raise HTTPException(status_code=400, detail="Invalid Kommo domain")

    access_token = payload.access_token or payload.api_key
    if not access_token:
        raise HTTPException(status_code=400, detail="Missing access token (api_key)")

    integ = db.query(models.KommoIntegration).filter(
        models.KommoIntegration.user_id == current_user.id
    ).first()

    if integ:
        integ.kommo_domain = domain
        integ.access_token = access_token
        integ.refresh_token = payload.refresh_token
        integ.webhook_secret = payload.webhook_secret
        integ.is_active = True
        integ.updated_at = datetime.utcnow()
    else:
        integ = models.KommoIntegration(
            user_id=current_user.id,
            kommo_domain=domain,
            access_token=access_token,
            refresh_token=payload.refresh_token,
            webhook_secret=payload.webhook_secret,
            is_active=True,
        )
        db.add(integ)

    # ensure user has an integration key (for /webhook/{integration_key})
    if not current_user.kommo_integration_key:
        import secrets
        current_user.kommo_integration_key = secrets.token_urlsafe(16)

    db.commit()
    db.refresh(integ)
    db.refresh(current_user)

    return {
        "status": "success",
        "message": "Kommo configured",
        "kommo_domain": integ.kommo_domain,
        "integration_key": current_user.kommo_integration_key,
        "webhook_url": _webhook_url(request, current_user.kommo_integration_key),
    }

# -------------------------------
# Optional: fetch/rotate key
# -------------------------------
@router.get("/integration/key")
async def get_integration_key(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user_for_api),
):
    if not current_user.kommo_integration_key:
        import secrets
        current_user.kommo_integration_key = secrets.token_urlsafe(16)
        db.commit()
        db.refresh(current_user)
    return {
        "integration_key": current_user.kommo_integration_key,
        "webhook_url": _webhook_url(request, current_user.kommo_integration_key),
    }

@router.post("/integration/key/rotate")
async def rotate_integration_key(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user_for_api),
):
    import secrets
    current_user.kommo_integration_key = secrets.token_urlsafe(16)
    db.commit()
    db.refresh(current_user)
    return {
        "integration_key": current_user.kommo_integration_key,
        "webhook_url": _webhook_url(request, current_user.kommo_integration_key),
    }

# -------------------------------
# Test stored credentials
# -------------------------------
@router.post("/integration/test")
async def test_integration(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user_for_api),
):
    integ = db.query(models.KommoIntegration).filter(
        models.KommoIntegration.user_id == current_user.id
    ).first()
    if not integ or not integ.is_active:
        raise HTTPException(status_code=400, detail="Kommo integration not configured")

    client = KommoClient(current_user.id, db)
    res = client.test_connection()
    if not res.get("success"):
        raise HTTPException(status_code=400, detail="Unable to reach Kommo API")

    return {"status": "ok"}

# -------------------------------
# Widget request endpoint
# -------------------------------
@router.post("/kommo/widget-request")
async def widget_request(payload: WidgetRequestPayload):
    """Handle inbound requests from the Kommo Salesbot widget."""
    source = payload.from_ or "unknown"
    logger.info(f"Received widget request from {source}: {payload.dict()}")
    return {"status": "ok"}

# -------------------------------
# Webhook receiver used by Salesbot
# -------------------------------
@router.post("/webhook/{integration_key}", name="kommo_webhook")
async def kommo_webhook(
    integration_key: str,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(
        models.User.kommo_integration_key == integration_key
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid integration key")

    body = await request.body()
    try:
        payload = json.loads(body.decode("utf-8"))
    except Exception:
        payload = {"raw": body.decode("utf-8", "ignore")}

    integ = db.query(models.KommoIntegration).filter(models.KommoIntegration.user_id == user.id).first()

    handler = KommoWebhookHandler(db)
    background_tasks.add_task(
        handler.process_webhook, user.id, payload, integ.webhook_secret if integ else None
    )

    logger.info("[Kommo] webhook received for user %s", user.id)
    return {"status": "ok"}
