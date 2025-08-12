from .states import OverallState
from langgraph.types import Command

def cart_builder_agent(state: OverallState):
    products = state.get("optimized_products", [])
    print(f"Cart builder received {len(products)} products")
    
    # Since Walmart API is not accessible, return a dummy cart URL
    cart_url = "https://walmart.com/cart" if products else ""
    print(f"Cart builder returning URL: {cart_url}")
    
    return {"cart_url": cart_url, "optimized_products": products}
