from fastapi import APIRouter, HTTPException, Query, status
from app.services.openfoodfacts_service import OpenFoodFactsService
import httpx # httpx is only needed here for its specific exceptions, not for making the core request

router = APIRouter(
    prefix="/openfoodfacts",
    tags=["Open Food Facts"]
)

@router.get("/search-product")
async def search_openfoodfacts_product(product_name: str = Query(..., description="The name of the product to search for.")):
    """
    Searches for a product on Open Food Facts by name and returns the first result.
    """
    print(f"Frontend requested search for: '{product_name}'") # Debug print
    service = OpenFoodFactsService()
    try:
        product = await service.search_product(product_name)
        if product:
            print(f"Backend returning product to frontend: {product.get('product_name')}") # Debug print
            return product
        # If product is None (no relevant product found)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No product found for '{product_name}' on Open Food Facts."
        )
    except httpx.RequestError as exc:
        print(f"HTTPX Request Error: {exc}") # Debug print
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not connect to Open Food Facts API: {exc}"
        )
    except httpx.HTTPStatusError as exc:
        print(f"HTTPX Status Error: {exc.response.status_code} - {exc.response.text}") # Debug print
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"Error from Open Food Facts API: {exc.response.text}"
        )
    except Exception as exc:
        print(f"General Exception in openfoodfacts router: {exc}") # Debug print
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {exc}"
        )