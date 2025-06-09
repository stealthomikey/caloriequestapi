import httpx
import urllib.parse # Used for URL encoding

class OpenFoodFactsService:
    # Use the v1 API endpoint with placeholders for search terms
    # Note: '{product_name}a' suggests an extra 'a' might be appended. I'll assume that's a typo
    # and use just '{product_name}' to directly insert the search term.
    BASE_URL_TEMPLATE = "https://world.openfoodfacts.org/cgi/search.pl?search_terms={product_name}&search_simple=1&json=1"

    async def search_product(self, product_name: str):
        # URL-encode the product name to ensure it's safe for a URL
        encoded_product_name = urllib.parse.quote_plus(product_name)
        
        # Construct the full URL by inserting the encoded product name
        full_url = self.BASE_URL_TEMPLATE.format(product_name=encoded_product_name)
        
        print(f"Searching Open Food Facts with v1 URL: {full_url}") # Debug print

        async with httpx.AsyncClient() as client:
            response = await client.get(full_url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            data = response.json()
            products = data.get("products")
            print(f"Open Food Facts API v1 response (first 3 products if any): {products[:3] if products else 'No products found'}") # Debug print

            if products:
                # Filter for products where the search terms are explicitly in the product name
                # This makes the search more precise, as v1 can be less strict.
                lower_product_name = product_name.lower()
                filtered_products = [
                    p for p in products
                    if lower_product_name in p.get("product_name", "").lower()
                ]

                if filtered_products:
                    print(f"Found exact match for '{product_name}': {filtered_products[0].get('product_name')}") # Debug print
                    return filtered_products[0]
                elif products: # If no exact match, but some products were returned, take the first one
                    print(f"No exact match found for '{product_name}', returning first available product: {products[0].get('product_name')}") # Debug print
                    return products[0]
            print(f"No products found for '{product_name}' after initial search.") # Debug print
            return None