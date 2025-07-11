# app/schemas.py

# import modules
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from datetime import datetime

# schema for user creation
class UserCreate(BaseModel):
    google_id: str
    email: str
    name: str

# schema for user display on frontend
class UserOut(BaseModel):
    id: int
    name: str
    email: str
    model_config = {'from_attributes': True} 

# schema for proudct creation
class ProductCreate(BaseModel):
    name: str
    brand: str
    quantity: str
    calories: float
    protein: float
    carbs: float
    fat: float

# schema for meal creation 
class MealCreate(BaseModel):
    product_id: int
    serving_size: float

# schema for meal output
class MealOut(BaseModel):
    product_id: int
    serving_size: float
    consumed_at: datetime
    model_config = {'from_attributes': True}

# schema for meal ingredients
class Ingredient(BaseModel):
    name: str
    measure: str

# schema for the meal db
class MealDB(BaseModel):
    idMeal: str
    strMeal: str
    strInstructions: str
    strMealThumb: HttpUrl
    strSource: Optional[HttpUrl] = None
    ingredients: List[Ingredient]
    model_config = {'from_attributes': True} 

# schema for the open food fact product for the barcode scanner
class Nutriments(BaseModel):
    energy_kcal_100g: Optional[float] = Field(None, alias="energy-kcal_100g")
    fat_100g: Optional[float] = None
    carbohydrates_100g: Optional[float] = None
    proteins_100g: Optional[float] = None

# schema for the open food fact product for the barcode scanner
class FoodProduct(BaseModel):
    code: str
    product_name: str
    image_url: Optional[HttpUrl] = None
    brand: Optional[str] = None
    quantity: Optional[str] = None
    serving_size: Optional[str] = None
    nutriments: Nutriments
    model_config = {'from_attributes': True} 

    # Assuming you already have these or similar
class ProductCreate(BaseModel):
    name: str

class MealCreate(BaseModel):
    product_id: int
    serving_size: float

class MealOut(MealCreate):
    id: int
    consumed_at: datetime

    class Config:
        from_attributes = True

# NEW SCHEMAS for food logging
class LoggedFoodCreate(BaseModel):
    product_name: str = Field(..., description="Name of the food product.")
    serving_size_g: float = Field(..., gt=0, description="Serving size in grams or ml.")
    calories: float = Field(..., ge=0, description="Total calories for the serving.")
    proteins: float = Field(..., ge=0, description="Total proteins for the serving.")
    carbohydrates: float = Field(..., ge=0, description="Total carbohydrates for the serving.")
    fats: float = Field(..., ge=0, description="Total fats for the serving.")

class LoggedFoodOut(LoggedFoodCreate):
    id: int
    user_id: int
    logged_at: datetime

    class Config:
        from_attributes = True