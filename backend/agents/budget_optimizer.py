from langchain_google_genai import ChatGoogleGenerativeAI
from states import OverallState
from typing import Dict, Any, List, Optional, Literal
from langgraph.types import Command

from dotenv import load_dotenv

load_dotenv()

def budget_optimizer_agent(state: OverallState) -> Command[Literal["cart_builder_agent"]]:
    """
    Uses LLM to select the best set of products under the user's budget.
    Returns: Command with {"optimized_products": [...]} and handoff to cart_builder_agent.
    """
    products: List[Dict[str, Any]] = state.get("products", [])
    budget: Optional[float] = state.get("budget")

    if not products or budget is None:
        return Command(update={"optimized_products": []}, goto="cart_builder_agent")

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    # Prepare a summary of product options for the LLM
    items_summary = []
    for prod in products:
        item = prod.get("item")
        options = prod.get("options", [])
        # Only include minimal info for each option
        options_summary = [
            {
                "name": opt.get("name"),
                "price": opt.get("price"),
                "brand": opt.get("brand"),
                "description": opt.get("description")
            }
            for opt in options
        ]
        items_summary.append({"item": item, "options": options_summary})

    prompt = (
        "You are a smart shopping assistant. "
        "Given a list of items, each with several product options (with price, brand, and description), "
        f"and a total budget of ${budget}, select the best combination of products so that the total price does not exceed the budget. "
        "Try to select one option per item. If the budget is too low, drop or substitute items as needed. "
        "Respond ONLY as a JSON array of selected product objects (with name, price, brand, and description). "
        "Example:\n"
        '[{"item": "milk", "name": "Great Value Milk", "price": 3.5, "brand": "Great Value", "description": "1 gallon whole milk"}, ...]\n\n'
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

    return Command(update={"optimized_products": optimized_products}, goto="cart_builder_agent")
