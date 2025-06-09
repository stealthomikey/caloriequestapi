# app/routers/food_logging.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import LoggedFoodCreate, LoggedFoodOut
from app.services import food_logging_service
from typing import List

router = APIRouter(
    prefix="/food-logs",
    tags=["Food Logging"]
)

@router.post("/", response_model=LoggedFoodOut)
async def log_food_for_user(
    food_data: LoggedFoodCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Logs a food item, automatically associating it with user_id=1 for development.
    """
    hardcoded_user_id = 1
    try:
        logged_food = await food_logging_service.log_food_item(db, hardcoded_user_id, food_data)
        return logged_food
    except Exception as e:
        print(f"Error logging food: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to log food item."
        )

@router.get("/history", response_model=List[LoggedFoodOut])
async def get_food_log_history(
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieves the logged food history for the hardcoded user_id=1 for development.
    """
    hardcoded_user_id = 1
    try:
        history = await food_logging_service.get_user_logged_food_history(db, hardcoded_user_id)
        return [LoggedFoodOut.model_validate(item) for item in history]
    except Exception as e:
        print(f"Error retrieving food history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve food history."
        )

# NEW ENDPOINT: DELETE /food-logs/{item_id}
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_food_log_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Deletes a specific logged food item by its ID.
    Requires the item to belong to the hardcoded user_id=1.
    """
    hardcoded_user_id = 1 # Match the user_id used for other operations
    try:
        deleted = await food_logging_service.delete_logged_food_item(db, item_id, hardcoded_user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Logged food item not found or does not belong to user."
            )
        # 204 No Content for successful deletion
        return {}
    except HTTPException as e:
        raise e # Re-raise HTTPExceptions from the service
    except Exception as e:
        print(f"Error deleting food item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete food item."
        )