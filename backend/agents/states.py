from typing_extensions import TypedDict, NotRequired, Literal, Optional
from typing import List, Dict, Any

# Input schema: what the graph expects as input
class InputInterpreterInputState(TypedDict):
    user_input: str
    user_id: NotRequired[str]  # Added for user authentication

# Output schema: what the graph will return as output
class InputInterpreterOutputState(TypedDict):
    cart_url: str
    optimized_products: Optional[List[Dict[str, Any]]]
    thread_id: NotRequired[str]  # Added for human-in-the-loop functionality
    interrupt: NotRequired[Dict[str, Any]]  # Added for human-in-the-loop functionality

# Overall state: union of all fields needed by all agents in the flow
class OverallState(TypedDict):
    # InputInterpreter fields
    user_input: str
    task_type: NotRequired[Literal["direct_product_list", "goal_or_dish"]]
    item_list: NotRequired[List[str]]
    budget: NotRequired[float]
    
    # User-related fields for personalization
    user_id: NotRequired[str]
    user_preferences: NotRequired[Dict[str, Any]]
    purchase_history: NotRequired[List[Dict[str, Any]]]

    # ItemExpansionAgent fields
    expanded_items: NotRequired[List[str]]

    # CategoryInferenceAgent fields
    categories: NotRequired[Dict[str, str]]  # item -> category

    # ProductSearchAgent fields
    products: NotRequired[List[Dict[str, Any]]]  # List of items with multiple product options

    # BudgetOptimizerAgent fields
    optimized_products: Optional[List[Dict[str, Any]]]

    # CartBuilderAgent fields
    cart_url: NotRequired[str]
    
    # Human-in-the-loop fields
    thread_id: NotRequired[str]
    interrupt_type: NotRequired[str]