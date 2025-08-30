import os
from pathlib import Path
from typing import Union
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class _Settings:

    # --- Security & Database ---
    @property
    def database_url(self) -> str:
        return os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    @property
    def secret_key(self) -> str:
        return os.getenv("SECRET_KEY", "a_very_secret_key_that_should_be_changed")
    
    @property
    def jwt_algorithm(self) -> str:
        return os.getenv("JWT_ALGORITHM", "HS256")
    
    @property
    def access_token_expire_minutes(self) -> int:
        return int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    # --- AI API Configuration ---
    # API keys should be set via environment variables
    @property
    def gemini_api_key(self) -> str:
        return os.getenv("GEMINI_API_KEY", "")
    
    @property
    def openai_api_key(self) -> str:
        return os.getenv("OPENAI_API_KEY", "")
    
    # Model configuration for chat generation
    @property
    def max_tokens(self) -> int:
        return int(os.getenv("MAX_TOKENS", "512"))
    
    @property
    def temperature(self) -> float:
        return float(os.getenv("TEMPERATURE", "0.7"))
    
    @property
    def max_history(self) -> int:
        return int(os.getenv("MAX_HISTORY", "4"))
    
    # --- Kommo Chat Integration Configuration ---
    @property
    def kommo_webhook_secret(self) -> str:
        return os.getenv("KOMO_WEBHOOK_SECRET", "")
    
    # --- CORS Configuration ---
    @property
    def cors_origins(self) -> list[str]:
        """
        CORS allowed origins. Can be set via CORS_ORIGINS environment variable
        as a comma-separated list. Defaults to common development origins.
        """
        origins_str = os.getenv("CORS_ORIGINS", "")
        if origins_str:
            return [origin.strip() for origin in origins_str.split(",")]
        
        # Default development origins
        return [
            "http://localhost:3000",  # Vue.js dev server
            "http://localhost:8000",  # FastAPI server
            "http://localhost:8001",  # Alternative port
            "http://127.0.0.1:3000",
            "http://127.0.0.1:8000", 
            "http://127.0.0.1:8001",
        ]
    
    @property
    def cors_allow_credentials(self) -> bool:
        return os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"

settings = _Settings()  # singleton

# --- Post-initialization logic ---
# Gemini API client will be initialized on first use
print("ℹ️ Using Gemini API for chat generation.")
