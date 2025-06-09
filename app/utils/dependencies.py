# app/utils/dependencies.py6

from fastapi import Request, HTTPException, status

# get current user id from request session
async def get_current_user_id(request: Request) -> int:
    user = request.session.get("user")
    if not user or "id" not in user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user["id"]