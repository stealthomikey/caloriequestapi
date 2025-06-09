# app/services/food_logging_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete # Import delete
from app.models import LoggedFoodItem, User
from app.schemas import LoggedFoodCreate, LoggedFoodOut
from typing import List, Optional # Import Optional

async def log_food_item(db: AsyncSession, user_id: int, food_data: LoggedFoodCreate) -> LoggedFoodItem:
    """
    Logs a food item with its calculated nutritional values for a specific user.
    """
    new_logged_food = LoggedFoodItem(
        user_id=user_id,
        product_name=food_data.product_name,
        serving_size_g=food_data.serving_size_g,
        calories=food_data.calories,
        proteins=food_data.proteins,
        carbohydrates=food_data.carbohydrates,
        fats=food_data.fats
    )
    db.add(new_logged_food)
    await db.commit()
    await db.refresh(new_logged_food)
    return new_logged_food

async def get_user_logged_food_history(db: AsyncSession, user_id: int) -> List[LoggedFoodItem]:
    """
    Retrieves the logged food item history for a specific user.
    """
    result = await db.execute(
        select(LoggedFoodItem).where(LoggedFoodItem.user_id == user_id).order_by(LoggedFoodItem.logged_at.desc())
    )
    return result.scalars().all()

# NEW FUNCTION: delete_logged_food_item
async def delete_logged_food_item(db: AsyncSession, item_id: int, user_id: int) -> bool:
    """
    Deletes a logged food item for a specific user by its ID.
    Returns True if deleted, False if not found or not owned by user.
    """
    # Select the item, ensuring it belongs to the user
    result = await db.execute(
        select(LoggedFoodItem).where(LoggedFoodItem.id == item_id, LoggedFoodItem.user_id == user_id)
    )
    item_to_delete = result.scalar_one_or_none()

    if item_to_delete:
        await db.delete(item_to_delete)
        await db.commit()
        return True
    return False