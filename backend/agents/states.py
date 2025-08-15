from typing_extensions import TypedDict, NotRequired, Literal, Optional
from typing import List, Dict, Any

class InputInterpreterInputState(TypedDict):
    user_input: str
    user_feedback: NotRequired[str]


class InputInterpreterOutputState(TypedDict):
    optimized_products: Optional[List[Dict[str, Any]]]

class OverallState(TypedDict):
    # InputInterpreter fields
    user_input: str
    task_type: NotRequired[Literal["direct_product_list", "goal_or_dish"]]
    item_list: NotRequired[List[str]]
    budget: NotRequired[float]
    
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
    