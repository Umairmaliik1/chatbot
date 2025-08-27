# app/kommo_client.py
import json
import logging
from datetime import datetime
from typing import Optional, Dict, List
import requests
from sqlalchemy.orm import Session

from . import models

logger = logging.getLogger(__name__)

def _normalize_domain(raw: str) -> str:
    """
    Accepts 'mycompany', 'mycompany.kommo.com', or full https URL
    Returns 'mycompany.kommo.com'
    """
    if not raw:
        return ""
    raw = raw.strip()
    raw = raw.replace("https://", "").replace("http://", "").rstrip("/")
    if "." not in raw:
        return f"{raw}.kommo.com"
    return raw

class KommoClient:
    """Kommo CRM API client per-user"""
    def __init__(self, user_id: int, db: Session):
        self.user_id = user_id
        self.db = db
        self.base_url: Optional[str] = None
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        self._load_integration_settings()

    def _load_integration_settings(self) -> bool:
        try:
            integ = self.db.query(models.KommoIntegration).filter(
                models.KommoIntegration.user_id == self.user_id
            ).first()

            if not integ or not integ.is_active:
                logger.warning(f"[Kommo] Integration inactive for user {self.user_id}")
                return False

            domain = _normalize_domain(integ.kommo_domain or "")
            if not domain:
                logger.error(f"[Kommo] Missing kommo_domain for user {self.user_id}")
                return False

            self.base_url = f"https://{domain}/api/v4"
            self.access_token = integ.access_token or ""
            self.refresh_token = integ.refresh_token
            self.token_expires_at = integ.token_expires_at
            logger.info(f"[Kommo] Base URL for user {self.user_id}: {self.base_url}")
            return True
        except Exception as e:
            logger.exception("[Kommo] Failed to load settings: %s", e)
            return False

    def _headers(self) -> Dict[str, str]:
        if not self.access_token:
            raise RuntimeError("No access token configured")
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _request(self, method: str, endpoint: str, *, params=None, json_body=None) -> Optional[Dict]:
        if not self.base_url:
            logger.error("[Kommo] base_url not set")
            return None

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            resp = requests.request(method.upper(), url, headers=self._headers(),
                                    params=params, json=json_body, timeout=15)
            if resp.status_code == 401:
                logger.warning("[Kommo] 401 from %s – token invalid/expired", url)
                # (Optional) implement refresh-token flow here if you use OAuth 2.0. See docs.  :contentReference[oaicite:3]{index=3}
                return None
            resp.raise_for_status()
            if resp.content:
                return resp.json()
            return {}
        except Exception as e:
            logger.exception("[Kommo] Request error %s %s: %s", method, url, e)
            return None

    # --- Convenience methods (subset) ---
    def test_connection(self) -> Dict:
        res = self._request("GET", "leads", params={"limit": 1})
        ok = bool(res)
        return {
            "success": ok,
            "message": "OK" if ok else "Failed",
            "raw": res if ok else None,
            "base_url": self.base_url,
        }

    def get_leads(self, limit: int = 50, page: int = 1) -> List[Dict]:
        res = self._request("GET", "leads", params={"limit": limit, "page": page})
        return (res or {}).get("_embedded", {}).get("leads", [])

    def get_contacts(self, limit: int = 50, page: int = 1) -> List[Dict]:
        res = self._request("GET", "contacts", params={"limit": limit, "page": page})
        return (res or {}).get("_embedded", {}).get("contacts", [])

    def get_deals(self, limit: int = 50, page: int = 1) -> List[Dict]:
        res = self._request("GET", "deals", params={"limit": limit, "page": page})
        return (res or {}).get("_embedded", {}).get("deals", [])
