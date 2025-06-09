# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Assuming you already have these models or similar
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    meals = relationship("UserMeal", back_populates="user")
    logged_foods = relationship("LoggedFoodItem", back_populates="user") # New relationship

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    # Add other product-specific fields you might have, e_g., openfoodfacts_id, name, etc.
    name = Column(String, unique=True, index=True) # Example field

    user_meals = relationship("UserMeal", back_populates="product")

class UserMeal(Base):
    __tablename__ = "user_meals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    serving_size = Column(Float)
    consumed_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="meals")
    product = relationship("Product", back_populates="user_meals")

# NEW MODEL: LoggedFoodItem
class LoggedFoodItem(Base):
    __tablename__ = "logged_food_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_name = Column(String, nullable=False) # Store the name at time of logging
    serving_size_g = Column(Float, nullable=False) # Store in grams/ml
    calories = Column(Float, nullable=False)
    proteins = Column(Float, nullable=False)
    carbohydrates = Column(Float, nullable=False)
    fats = Column(Float, nullable=False)
    logged_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="logged_foods")