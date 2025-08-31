import base64
import os
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken


_fernet: Optional[Fernet] = None


def _get_key() -> bytes:
    """Return the Fernet key from env var DATA_ENCRYPTION_KEY or derive from SECRET_KEY.

    - Prefer `DATA_ENCRYPTION_KEY` as a base64-encoded 32-byte key (Fernet key format).
    - If not set, derive a stable key from `SECRET_KEY` by hashing and base64-url encoding
      to 32 bytes. This is a fallback; production should explicitly set DATA_ENCRYPTION_KEY.
    """
    key_b64 = os.getenv("DATA_ENCRYPTION_KEY")
    if key_b64:
        try:
            # Validate by constructing Fernet
            Fernet(key_b64)
            return key_b64.encode()
        except Exception:
            raise ValueError(
                "Invalid DATA_ENCRYPTION_KEY. It must be a base64-encoded 32-byte key (Fernet)."
            )

    # Fallback: derive from SECRET_KEY deterministically (not ideal for rotation)
    secret = os.getenv("SECRET_KEY", "fallback-secret-key").encode()
    import hashlib

    digest = hashlib.sha256(secret).digest()  # 32 bytes
    # Fernet key must be urlsafe base64-encoded 32-byte key
    return base64.urlsafe_b64encode(digest)


def _get_fernet() -> Fernet:
    global _fernet
    if _fernet is None:
        _fernet = Fernet(_get_key())
    return _fernet


def encrypt(plaintext: Optional[str]) -> Optional[str]:
    """Encrypt plaintext to a base64 token. Returns None if input is falsy."""
    if not plaintext:
        return None
    f = _get_fernet()
    token = f.encrypt(plaintext.encode("utf-8"))
    return token.decode("utf-8")


def decrypt(token: Optional[str]) -> Optional[str]:
    """Decrypt base64 token to plaintext. Returns None if input is falsy or invalid."""
    if not token:
        return None
    f = _get_fernet()
    try:
        plain = f.decrypt(token.encode("utf-8"))
        return plain.decode("utf-8")
    except (InvalidToken, ValueError):
        return None

