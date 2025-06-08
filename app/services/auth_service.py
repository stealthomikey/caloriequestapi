# app/services/auth_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User
from app.schemas import UserCreate

# gets or creates a user based on Google OAuth information
async def get_or_create_user(db: AsyncSession, user_info: dict) -> User:
    result = await db.execute(select(User).filter(User.google_id == user_info["sub"]))
    user = result.scalars().first()

    if not user:
        user = User(
            google_id=user_info["sub"],
            email=user_info["email"],
            name=user_info["name"]
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user