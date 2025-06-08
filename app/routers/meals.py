# app/routers/meals.py

from fastapi import APIRouter, Query, HTTPException, status
from typing import List, Annotated
from app.services.mealdb_service import search_meals_by_name, get_random_meals, get_meal_by_id
from app.schemas import MealDB

router = APIRouter(
    prefix="/meals",
    tags=["Meals (TheMealDB)"]
)

SearchQuery = Annotated[
    str,
    Query(min_length=2, description="Meal name.")
]

# route to get random meals
@router.get("/suggestions", response_model=List[MealDB])
async def get_meal_suggestions():
    return await get_random_meals(count=6)

# route for user searching meals by name
@router.get("/search", response_model=List[MealDB])
async def search_meals(query: SearchQuery):
    meals = await search_meals_by_name(query=query, limit=12)
    if not meals:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No meals found matching '{query}'."
        )
    return meals

# route to get meals by id for recipe page
@router.get("/{meal_id}", response_model=MealDB)
async def get_meal_details(meal_id: str):
    meal = await get_meal_by_id(meal_id)
    if not meal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meal with ID '{meal_id}' not found."
        )
    return meal