import secrets
from fastapi import APIRouter, Request, Depends, Form
from datetime import timedelta
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional
from .. import models, hashing, auth
from ..database import get_db

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, message: Optional[str] = None):
    """Renders the login page - now handled by Vue.js frontend."""
    from fastapi.responses import FileResponse
    return FileResponse("static/dist/index.html")

@router.post("/login")
async def handle_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    remember_me: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # The form uses 'username', so we query by username.
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user or not hashing.Hash.verify(user.hashed_password, password):
        # On error, re-render the login page with an error message.
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # The JWT 'sub' (subject) should still be the username for consistency with auth logic.
    expires_delta = None
    if remember_me:
        # Set a longer expiration for "Remember Me", e.g., 30 days
        expires_delta = timedelta(days=30)

    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=expires_delta)
    
    # Return redirect for HTML form submissions
    response = RedirectResponse(url="/dashboard", status_code=302)
    # Add headers to prevent the browser from caching this redirect
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@router.post("/api/login")
async def handle_login_api(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    remember_me: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """API endpoint for Vue.js frontend login."""
    # The form uses 'username', so we query by username.
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user or not hashing.Hash.verify(user.hashed_password, password):
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # The JWT 'sub' (subject) should still be the username for consistency with auth logic.
    expires_delta = None
    if remember_me:
        # Set a longer expiration for "Remember Me", e.g., 30 days
        expires_delta = timedelta(days=30)

    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=expires_delta)
    
    # Return JSON response for API calls with full user + profile so frontend can render immediately
    from fastapi.responses import JSONResponse
    # Ensure profile is loaded
    profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user.id).first()
    user_payload = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "kommo_integration_key": user.kommo_integration_key,
    }
    if profile:
        user_payload["profile"] = {
            "xelence_affiliateid": profile.xelence_affiliateid,
            "xelence_x_api_key": profile.xelence_x_api_key,
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "chat_rate": profile.chat_rate,
            "kommo_widget_installed": profile.kommo_widget_installed,
            # AI settings
            "response_delay_seconds": profile.response_delay_seconds,
            "ai_provider": profile.ai_provider,
            # User customization
            "custom_logo_url": profile.custom_logo_url,
            "custom_favicon_url": profile.custom_favicon_url,
            "custom_website_name": profile.custom_website_name,
        }
    response = JSONResponse(content={"message": "Login successful", "user": user_payload})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@router.get("/logout", status_code=302)
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie(key="access_token")
    return response

@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request, error: Optional[str] = None):
     """Renders the forgot password page - now handled by Vue.js frontend."""
     from fastapi.responses import FileResponse
     return FileResponse("static/dist/index.html")

@router.post("/forgot-password")
async def handle_forgot_password(request: Request, username: str = Form(...), db: Session = Depends(get_db)):
    """Handles the forgot password request."""
    #Basic implementation.  A real implementation would email a reset link.
    from fastapi.responses import JSONResponse
    return JSONResponse(content={"message": "Password reset email sent (not really)."})

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    """Renders the user signup page - now handled by Vue.js frontend."""
    from fastapi.responses import FileResponse
    return FileResponse("static/dist/index.html")

@router.post("/signup")
async def handle_signup(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handles user registration."""
    from fastapi import HTTPException
    
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists.")

    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long.")

    new_user = models.User(
        username=username,
        hashed_password=hashing.Hash.bcrypt(password),
        kommo_integration_key=secrets.token_urlsafe(9),
        profile=models.UserProfile()
    )
    db.add(new_user)
    db.commit()

    # Redirect to login page with a success message
    return RedirectResponse(url="/login?message=Signup successful! Please log in.", status_code=302)

@router.post("/api/signup")
async def handle_signup_api(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    """API endpoint for Vue.js frontend signup."""
    from fastapi import HTTPException
    from fastapi.responses import JSONResponse
    
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists.")

    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long.")

    new_user = models.User(
        username=username,
        hashed_password=hashing.Hash.bcrypt(password),
        kommo_integration_key=secrets.token_urlsafe(9),
        profile=models.UserProfile()
    )
    db.add(new_user)
    db.commit()

    # Return JSON response for API calls
    return JSONResponse(content={"message": "Signup successful! Please log in.", "user": {"id": new_user.id, "username": new_user.username}})

@router.get("/auth/me")
async def get_current_user_api(user: models.User = Depends(auth.get_current_user_for_api), db: Session = Depends(get_db)):
    """API endpoint to get the current authenticated user."""
    try:
        # Load the user profile to get Xelence credentials
        profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user.id).first()
        
        return {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "kommo_integration_key": user.kommo_integration_key,
                "profile": {
                    "xelence_affiliateid": profile.xelence_affiliateid if profile else None,
                    "xelence_x_api_key": profile.xelence_x_api_key if profile else None,
                    "first_name": profile.first_name if profile else None,
                    "last_name": profile.last_name if profile else None,
                    "chat_rate": profile.chat_rate if profile else None,
                    "kommo_widget_installed": profile.kommo_widget_installed if profile else False,
                    # AI settings
                    "response_delay_seconds": profile.response_delay_seconds if profile else None,
                    "ai_provider": profile.ai_provider if profile else None,
                    # User customization
                    "custom_logo_url": profile.custom_logo_url if profile else None,
                    "custom_favicon_url": profile.custom_favicon_url if profile else None,
                    "custom_website_name": profile.custom_website_name if profile else None,
                } if profile else None
            }
        }
    except Exception as e:
        # Log the error and return a basic user object without profile
        print(f"Error in /auth/me endpoint: {e}")
        return {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "kommo_integration_key": user.kommo_integration_key,
                "profile": None
            }
        }
