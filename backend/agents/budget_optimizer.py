from langchain_google_genai import ChatGoogleGenerativeAI
from .states import OverallState
from typing import Dict, Any, List, Optional, Literal
from langgraph.types import Command, interrupt
from .personalization import personalize_product_selection

from dotenv import load_dotenv

load_dotenv()

def budget_optimizer_agent(state: OverallState) -> Command[Literal["cart_builder_agent"]]:
    """
    Uses LLM to select the best set of products under the user's budget.
    Returns: Command with {"optimized_products": [...]} and handoff to cart_builder_agent.
    """
    products: List[Dict[str, Any]] = state.get("products", [])
    budget: Optional[float] = state.get("budget")
    print(f"Budget optimizer received {len(products)} products, budget: {budget}")

    if not products or budget is None:
        print("No products or budget, returning empty")
        return Command(update={"optimized_products": []}, goto="cart_builder_agent")

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    # Prepare a summary of product options for the LLM
    items_summary = []
    for prod in products:
        item = prod.get("item")
        category = prod.get("category")
        options = prod.get("options", [])
        # Include all relevant info for each option
        options_summary = [
            {
                "name": opt.get("name"),
                "price": opt.get("price"),
                "rating": opt.get("rating"),
                "brand": opt.get("brand"),
                "category": opt.get("category", category),
                "description": opt.get("description")
            }
            for opt in options if opt.get("price") is not None
        ]
        items_summary.append({"item": item, "category": category, "options": options_summary})

    prompt = (
        "You are a smart shopping assistant. "
        "Given a list of items, each with several product options (with name, price, rating, brand, category, and description), "
        f"and a total budget of ${budget}, select the best combination of products so that the total price does not exceed the budget. "
        "Consider both price and rating when making selections. Try to select one option per item. If the budget is too low, drop or substitute items as needed. "
        "Respond ONLY as a JSON array of selected product objects (with item, name, price, rating, brand, category, and description). "
        "Example:\n"
        '[{"item": "milk", "name": "Great Value Milk", "price": 3.5, "rating": 4.2, "brand": "Great Value", "category": "dairy", "description": "1 gallon whole milk"}, ...]\n\n'
        f"Items and options: {items_summary}"
    )

    response = llm.invoke([{"role": "user", "content": prompt}])

    try:
        import json
        content = response.content.strip()
        # Remove markdown code blocks if present
        if content.startswith('```json'):
            content = content[7:]  # Remove ```json
        if content.endswith('```'):
            content = content[:-3]  # Remove ```
        content = content.strip()
        optimized_products = json.loads(content)
        if not isinstance(optimized_products, list):
            optimized_products = []
    except Exception as e:
        print(f"JSON parsing error: {e}")
        optimized_products = []

    # Add human review interrupt
    if optimized_products:
        optimized_products = interrupt({
            "type": "optimization_review",
            "optimized_products": optimized_products,
            "budget": budget,
            "message": "Please review the optimized product selections."
        })
    
    return Command(update={"optimized_products": optimized_products, "interrupt_type": "optimization_review"}, goto="cart_builder_agent")


