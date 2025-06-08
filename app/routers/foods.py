from fastapi import APIRouter, HTTPException, status
from typing import Optional

# Import the service function that calls the Open Food Facts API
from app.services.scanner_service import get_product_by_barcode

# Import the Pydantic model that defines the shape of the response
from app.schemas import FoodProduct

router = APIRouter(
    prefix="/products",   # The URL prefix for all routes in this file
    tags=["Products (Open Food Facts)"]   # The group name for the API docs
)

# route with barcode to get proudcct details
@router.get("/{barcode}", response_model=FoodProduct)
async def get_product_details(barcode: str):
    # 1. searches for product by barcode
    product = await get_product_by_barcode(barcode)
    
    if not product:
        # error handling
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with barcode '{barcode}' not found."
        )
        
    # return found product
    return product