# app/routers/user_actions.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas import ProductCreate, MealCreate, MealOut, UserOut # <-- Import UserOut
from app.services import db_service
from app.utils.dependencies import get_current_user_id # <-- CORRECTED IMPORT PATH

# set up router for user actions
router = APIRouter(
    prefix="/user",
    tags=["User Actions"]
)

# route to create a new product
@router.post("/products", status_code=status.HTTP_201_CREATED)
# create a new proudct for the user
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    try: 
        return await db_service.add_product(db, product_data)
    except Exception as e:
        print(f"Error creating product: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create product.")

# route to log a meal for the user
@router.post("/meals/log", response_model=MealOut, status_code=status.HTTP_201_CREATED)
async def log_meal(
    meal_data: MealCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    try: 
        logged_meal = await db_service.log_user_meal(db, user_id, meal_data)
        return logged_meal
    except Exception as e:
        print(f"Error logging meal: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to log meal.")

# route to get the meal history for the user
@router.get("/meals", response_model=List[MealOut])
async def get_user_meals(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    try:
        meals = await db_service.fetch_user_meals(db, user_id)
        return meals
    except Exception as e:
        print(f"Error fetching user meals: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve user meals.")

# get current users deatils eg name 
@router.get("/me", response_model=UserOut, summary="Get current authenticated user details")
async def get_current_user_details(
    request: Request, # Need Request to access session
    user_id: int = Depends(get_current_user_id) # Ensure user is logged in
):
    user_session_info = request.session.get("user")
    if not user_session_info:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found in session.")

    return UserOut(
        id=user_session_info["id"],
        name=user_session_info["name"],
        email=user_session_info["email"]
    )

from app.schemas import ProductOut # Ensure ProductOut is imported

@router.get("/products", response_model=List[ProductOut], summary="Get all products added by the current user")
async def get_user_products(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    try:
        products = await db_service.fetch_user_products(db, user_id)
        return products
    except Exception as e:
        print(f"Error fetching user products: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve user products.")