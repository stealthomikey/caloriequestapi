from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Product, UserMeal, User
from app.schemas import ProductCreate, MealCreate, MealOut
from typing import List, Optional

# add a new product to the database
async def add_product(db: AsyncSession, product_data: ProductCreate) -> Product:
    new_product = Product(**product_data.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

# logs a meal fro the user
async def log_user_meal(db: AsyncSession, user_id: int, meal_data: MealCreate) -> UserMeal:
    new_meal = UserMeal(
        user_id=user_id,
        product_id=meal_data.product_id,
        serving_size=meal_data.serving_size
    )
    db.add(new_meal)
    await db.commit()
    await db.refresh(new_meal)
    return new_meal

# retrieves the meal history for a user
async def get_user_meal_history(db: AsyncSession, user_id: int) -> List[UserMeal]:
    """
    Retrieves the meal history for a specific user.
    """
    result = await db.execute(
        select(UserMeal).where(UserMeal.user_id == user_id).order_by(UserMeal.consumed_at.desc())
    )
    return result.scalars().all()