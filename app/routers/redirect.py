# app/routers/auth_redirect.py

from fastapi import APIRouter, Request, Depends, HTTPException, status
from starlette.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.utils.oauth import oauth
from app.services.auth_service import get_or_create_user

router = APIRouter(prefix="/auth", tags=["Auth Redirect"])

# front end redirect url after login
FRONTEND_REDIRECT_URL = "http://localhost:3000/"
# error redirect 
FRONTEND_LOGOUT_REDIRECT_URL = "http://localhost:3000/"

# login route to initiate Google OAuth
@router.get("/login", summary="Initiate Google OAuth login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

# OAuth callback route to handle the response from Google
@router.get("/callback", summary="Google OAuth callback handler")
async def auth_callback(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")
        if not user_info:
            print("OAuth callback: No user info received from Google.")
            return RedirectResponse(url=f"{FRONTEND_LOGOUT_REDIRECT_URL}?error=oauth_failed")

        user = await get_or_create_user(db, user_info)
        request.session["user"] = {"id": user.id, "email": user.email, "name": user.name}

        # Redirect to the frontend URL after successful login
        return RedirectResponse(url=FRONTEND_REDIRECT_URL)
    except Exception as e:
        print(f"Error during OAuth callback: {e}")
        # Redirect to frontend with an error message in case of login failure
        return RedirectResponse(url=f"{FRONTEND_LOGOUT_REDIRECT_URL}?error=auth_failed&message={e}")

# logout route and clear session
@router.get("/logout", summary="Log out the current user")
async def logout(request: Request):
    request.session.clear()
    # Redirect to frontend again
    return RedirectResponse(url=FRONTEND_LOGOUT_REDIRECT_URL)