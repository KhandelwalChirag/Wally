from agents.states import OverallState
from typing import Dict, Any, List
import urllib.parse

def build_walmart_cart_url(products: List[Dict[str, Any]]) -> str:
    """
    Constructs a pre-filled cart URL for Walmart.com.
    This is a simplified example. The actual API/URL structure may differ.
    """
    if not products:
        return ""
    
    # This is a hypothetical URL structure. You would need to find the actual
    # format for pre-filling a Walmart cart, which often involves specific product IDs (SKUs).
    # For this example, we'll just create a search query.
    base_url = "[https://www.walmart.com/search?q=](https://www.walmart.com/search?q=)"
    
    product_names = [p.get("name", "") for p in products]
    query = " ".join(product_names)
    
    return base_url + urllib.parse.quote(query)


def cart_builder_agent(state: OverallState) -> Dict[str, str]:
    """
    Builds a cart URL from the final list of products.
    Returns a dictionary with the 'cart_url'.
    """
    products = state.get("optimized_products", [])
    
    if not products:
        # If optimization failed or returned nothing, use the raw products
        products = state.get("products", [])
        # Flatten the raw products list
        if products and "options" in products[0]:
             products = [opt for prod in products for opt in prod.get("options", [])]


    cart_url = build_walmart_cart_url(products)

    return {"cart_url": cart_url}
