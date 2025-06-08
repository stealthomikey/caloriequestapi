# mealdb_service.py

import httpx
import asyncio
from typing import List, Dict, Any

class MealServiceError(Exception):
    pass

# gets raw data from api and structures it
def _transform_meal_data(raw_meal: Dict[str, Any]) -> Dict[str, Any]:
    if not raw_meal:
        return {}
    
    # process ingredients, stop when no more are found (max 20)
    ingredients = []
    for i in range(1, 21):
        ingredient_name = raw_meal.get(f'strIngredient{i}')
        measure = raw_meal.get(f'strMeasure{i}')
        if ingredient_name and ingredient_name.strip():
            ingredients.append({"name": ingredient_name, "measure": measure or ""})
        else:
            # No more ingredients
            break
            
    # get the source URL
    source_url = raw_meal.get('strSource')

    # Return the data
    return {
        "idMeal": raw_meal.get('idMeal'),
        "strMeal": raw_meal.get('strMeal'),
        "strInstructions": raw_meal.get('strInstructions'),
        "strMealThumb": raw_meal.get('strMealThumb'),
        "strSource": source_url if source_url and source_url.strip() else None,
        "ingredients": ingredients
    }

# gets meal from search name
async def search_meals_by_name(query: str, limit: int = 12) -> List[Dict[str, Any]]:
    api_url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()
        
        data = response.json()
        raw_meals = data.get('meals')
        
        if not raw_meals:
            return []
            
        transformed_meals = [_transform_meal_data(meal) for meal in raw_meals]
        return transformed_meals[:limit]
        
    except httpx.RequestError as e:
        raise MealServiceError(f"Error connecting to TheMealDB API: {e}")

# retrieves a 6 random meals from TheMealDB API
async def get_random_meals(count: int = 6) -> List[Dict[str, Any]]:
    api_url = "https://www.themealdb.com/api/json/v1/1/random.php"
    try:
        async with httpx.AsyncClient() as client:
            # Create a list of concurrent tasks
            tasks = [client.get(api_url) for _ in range(count)]
            responses = await asyncio.gather(*tasks)
            
        meals = []
        for res in responses:
            res.raise_for_status()
            raw_meal = res.json().get('meals')[0]
            meals.append(_transform_meal_data(raw_meal))
            
        return meals
        
    except httpx.RequestError as e:
        raise MealServiceError(f"Error connecting to TheMealDB API: {e}")

# retrieves a meal by its ID from TheMealDB API
async def get_meal_by_id(meal_id: str) -> Dict[str, Any]:
    api_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()
        
        data = response.json()
        
        raw_meals = data.get('meals')
        
        if not raw_meals:
            return {}

        return _transform_meal_data(raw_meals[0])
            
    except httpx.RequestError as e:
        raise MealServiceError(f"Error connecting to TheMealDB API: {e}")