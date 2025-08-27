# app/main.py
from contextlib import asynccontextmanager
import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from .settings import settings
from .routers import reports, auth_pages, dashboard_pages, chat_api, user_api, instructions_api, kommo_api
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI): # pylint: disable=W0613
    """Lifespan manager for application startup/shutdown."""
    print("--- Initializing LangChain Gemini client ---")
    print("\n" + "="*80)
    print("✅✅✅ SERVER HAS STARTED/RELOADED! ✅✅✅")
    print("If you see this message, your code changes are being loaded correctly.")
    print("="*80 + "\n")
    print("🚀 Application startup complete. LangChain Gemini client is ready.")
    yield
    print("🔌 Application shutdown.")

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# Add session middleware for flash messages
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# Include the router for our /api/reports endpoint
app.include_router(reports.router, prefix="/api", tags=["reports"])
app.include_router(auth_pages.router, tags=["Authentication"])
app.include_router(dashboard_pages.router, tags=["Dashboard"])
app.include_router(chat_api.router, prefix="/api", tags=["chat"])
app.include_router(user_api.router)
app.include_router(instructions_api.router, prefix="/api", tags=["instructions"])
app.include_router(kommo_api.router)

@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    """
    Middleware to add Cache-Control headers to prevent browser caching
    for all dashboard-related pages. This is crucial for ensuring
    authentication checks are always performed.
    """
    response = await call_next(request)
    # We need to ensure that both the HTML pages and the static assets they load
    # are not cached by the browser, especially during development.
    if request.url.path.startswith(("/dashboard", "/static", "/css")):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

# Templates removed - using Vue.js frontend

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Serves the application's favicon."""
    return FileResponse("static/dist/assets/logo.svg")

# ----------------- 4) STATIC FILES AT ROOT -----------------
# Old template directories removed - using Vue.js frontend

# Mount the primary static directory for JS, etc., under a specific path
# to avoid conflicts with API routes like /dashboard.
app.mount("/static", StaticFiles(directory="static"), name="static_files")

# Mount the Vue.js dist directory to serve the built frontend assets
app.mount("/assets", StaticFiles(directory="static/dist/assets"), name="frontend_assets")

# Serve Vue.js frontend for all non-API routes
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str, request: Request):
    """
    Serve Vue.js frontend for all non-API routes.
    This allows Vue Router to handle client-side routing.
    """
    # Don't serve frontend for API routes
    if full_path.startswith(("api/", "css/", "images/", "static/", "favicon.ico")):
        return {"error": "Not found"}
    
    # Serve the Vue.js index.html for all other routes
    try:
        return FileResponse("static/dist/index.html")
    except FileNotFoundError:
        # Fallback to development mode - redirect to frontend dev server
        return {"message": "Frontend not built. Please run 'npm run build' in the frontend directory or access the frontend directly at http://localhost:3000"}
