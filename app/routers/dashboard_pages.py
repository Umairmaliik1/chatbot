from pathlib import Path
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
# Templates removed - using Vue.js frontend
from sqlalchemy.orm import Session

from .. import auth, models, database
from ..settings import settings
from ..flash import flash, get_flashed_messages
import secrets

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    # The dependency is now injected into each route individually for clarity.
    # dependencies=[Depends(auth.get_current_user_for_page)],
)

# Templates removed - using Vue.js frontend

def _get_template_context(request: Request, user: models.User, **kwargs):
    """
    Helper to build the context dictionary for templates, ensuring
    common variables are always present.
    """
    # The user is now passed in explicitly.
    context = {
        "request": request,
        "current_user": user,
        "user": user, # for backwards compatibility with some templates

        "messages": get_flashed_messages(request),
    }
    context.update(kwargs)
    return context

@router.get("/", response_class=HTMLResponse, name="dashboard_home")
async def dashboard_home(request: Request, user: models.User = Depends(auth.get_current_user_for_page)):
    if isinstance(user, RedirectResponse):
        return user
    from fastapi.responses import FileResponse
    return FileResponse("static/dist/index.html")

@router.get("/chat", response_class=HTMLResponse, name="chat_history")
async def chat_history_page(request: Request, user: models.User = Depends(auth.get_current_user_for_page)):
    if isinstance(user, RedirectResponse):
        return user
    from fastapi.responses import FileResponse
    return FileResponse("static/dist/index.html")

@router.get("/analytics", response_class=HTMLResponse, name="analytics")
async def analytics_page(request: Request, user: models.User = Depends(auth.get_current_user_for_page)):
    if isinstance(user, RedirectResponse):
        return user
    from fastapi.responses import FileResponse
    return FileResponse("static/dist/index.html")

@router.get("/reports", response_class=HTMLResponse, name="reports")
async def reports_page(request: Request, user: models.User = Depends(auth.get_current_user_for_page)):
    if isinstance(user, RedirectResponse):
        return user
    from fastapi.responses import FileResponse
    return FileResponse("static/dist/index.html")

@router.get("/instructions", response_class=HTMLResponse, name="instructions")
async def instructions_page(request: Request, user: models.User = Depends(auth.get_current_user_for_page)):
    if isinstance(user, RedirectResponse):
        return user
    from fastapi.responses import FileResponse
    return FileResponse("static/dist/index.html")

@router.get("/testchat", response_class=HTMLResponse, name="testchat")
async def testchat_page(request: Request, user: models.User = Depends(auth.get_current_user_for_page)):
    if isinstance(user, RedirectResponse):
        return user
    from fastapi.responses import FileResponse
    return FileResponse("static/dist/index.html")

@router.get("/kommo", response_class=HTMLResponse, name="kommo")
async def kommo_page(
    request: Request,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(auth.get_current_user_for_page)
):
    if isinstance(user, RedirectResponse):
        return user
    if not user.kommo_integration_key:
        user.kommo_integration_key = secrets.token_urlsafe(16)
        db.commit()
        db.refresh(user)
    from fastapi.responses import FileResponse
    return FileResponse("static/dist/index.html")

@router.get("/settings", response_class=HTMLResponse, name="settings")
async def settings_page(
    request: Request, 
    db: Session = Depends(database.get_db),
    user: models.User = Depends(auth.get_current_user_for_page)
):
    if isinstance(user, RedirectResponse):
        return user
    # Ensure a profile object exists for the user before rendering the page.
    # This prevents an error if a user has never saved their API settings.
    if not user.profile:
        new_profile = models.UserProfile(user_id=user.id)
        db.add(new_profile)
        db.commit()
        db.refresh(user) # Refresh the user object to load the new profile
    from fastapi.responses import FileResponse
    return FileResponse("static/dist/index.html")

# --- Form Submission Endpoints for Settings Page ---


@router.post("/update-api-settings", name="update_api_settings")
async def update_api_settings(
    request: Request,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(auth.get_current_user_for_page),
    xelence_affiliateid: str = Form(None),
    xelence_x_api_key: str = Form(None)
):
    if isinstance(user, RedirectResponse):
        return user
    profile = user.profile
    if not profile:
        profile = models.UserProfile(user_id=user.id)
        db.add(profile)

    profile.xelence_affiliateid = xelence_affiliateid
    if xelence_x_api_key and xelence_x_api_key != '••••••••':
        profile.xelence_x_api_key = xelence_x_api_key

    db.commit()
    flash(request, "API settings updated successfully!", "success")
    return RedirectResponse(url=request.url_for("settings"), status_code=303)