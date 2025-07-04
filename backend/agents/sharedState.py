from typing_extensions import TypedDict, Annotated
from typing import List, Dict, Optional, Literal
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class Product(TypedDict, total=False):
    name: str
    price: float
    brand: Optional[str]
    productRating : float
    description: Optional[str]
    walmart_category: str

class SharedState(TypedDict, total=False):
    # Raw user input (string)
    user_input: str
    # Parsed budget (if any, if not then pick the highest rated item)
    budget: Optional[float]
    # Task type: "direct_product_list" or "goal_or_dish"
    task_type: Optional[Literal["direct_product_list", "goal_or_dish"]]
    task : str
    # List of items parsed from input (direct or expanded)
    item_list: List[Dict[str, str]]
    # List of dicts: item name + inferred category
    categorized_items: List[Dict[str, str]]
    # Search results: list of lists of Product dicts (one list per item)
    search_results: List[List[Product]]
    # Optimized cart: list of selected Product dicts
    optimized_cart: List[Product]
    # Cart ID or URL after cart creation
    cart_id: Optional[str]
    # Message history for human-in-the-loop or debugging
    messages: Annotated[List[AnyMessage], add_messages]