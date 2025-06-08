import httpx
from typing import Dict, Any, Optional

# error handling
class FoodFactsServiceError(Exception):
    pass

# filters the product data we get from the open food api
def _transform_product_data(product_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not product_data or "product" not in product_data:
        return None
    product = product_data["product"]
    if not product.get("product_name") or not product.get("nutriments"):
        return None
    # extract from json via the nutriments section
    nutriments = product.get("nutriments", {})
    def get_nutrient(key: str) -> Optional[float]:
        value = nutriments.get(f"{key}_100g", nutriments.get(key, 0))
        return round(float(value), 2) if isinstance(value, (int, float)) else None
    # package the data into a dictionary
    return {
        "code": product.get("code"),
        "product_name": product.get("product_name"),
        "image_url": product.get("image_front_url"),
        "brand": product.get("brands"),
        "quantity": product.get("quantity"),
        "serving_size": product.get("serving_size"),
        "nutriments": {
            "energy-kcal_100g": get_nutrient("energy-kcal"),
            "fat_100g": get_nutrient("fat"),
            "carbohydrates_100g": get_nutrient("carbohydrates"),
            "proteins_100g": get_nutrient("proteins"),
        }
    }

# retrieves the product data from the open food fact api via the barcode 
async def get_product_by_barcode(barcode: str) -> Optional[Dict[str, Any]]:

    # search the api with the barcode 
    api_url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    try:
        async with httpx.AsyncClient() as client:
            # gets product data from api
            response = await client.get(api_url)
            response.raise_for_status()
        # gets the response data as json
        data = response.json()
        
        # return none if no product data is found
        if data.get("status") == 0:
            return None
        
        return _transform_product_data(data)
    # error handling
    except httpx.RequestError as e:
        raise FoodFactsServiceError(f"Error connecting to Open Food Facts API: {e}")