# app/routers/auth_router.py

from fastapi import APIRouter, Request, Depends
from starlette.responses import RedirectResponse
from app.database import get_db
from app.utils.oauth import oauth
from app.services.auth_service import get_or_create_user
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status # Removed redundant Request, Depends imports

# Create a new API router
router = APIRouter(prefix="/auth", tags=["auth"])



# Route to initiate the Google Oauth login process
@router.get("/login", summary="Initiate Google OAuth Login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

# O auth callback route to handle the response from Google
@router.get("/callback", summary="Google OAuth Callback Handler")
async def auth_callback(request: Request, db: AsyncSession = Depends(get_db)):
    # gets access token from Google
    token = await oauth.google.authorize_access_token(request)
    # gets user information from the token
    user_info = token.get("userinfo")
    
    # Get or create the user in our database based on Google user info
    user = await get_or_create_user(db, user_info)
    
    # stores essential user information in the session
    request.session["user"] = {"id": user.id, "email": user.email}
    
    # Redirect to the api dashboard after successful authentication which will be redirected to the frontend
    return RedirectResponse(url="/dashboard")

# Route to log out the current user
@router.get("/logout", summary="Log out the current user")
async def logout(request: Request):
    # clear all data from the session
    request.session.clear() 
    return RedirectResponse(url="/") 

# get the user id from the session 
async def get_current_user_id(request: Request) -> int:
    user = request.session.get("user")
    # Check if user data exists in the session and contains an id
    if not user or "id" not in user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}, 
        )
    return user["id"]

