from langchain_google_genai import ChatGoogleGenerativeAI
from agents.states import OverallState
from typing import Dict, Any, List, Optional
import json
from dotenv import load_dotenv

load_dotenv()

def budget_optimizer_agent(state: OverallState) -> Dict[str, Any]:
    """
    Uses LLM to select the best set of products under the user's budget.
    Returns a dictionary with the 'optimized_products' update.
    """
    products: List[Dict[str, Any]] = state.get("products", [])
    budget: Optional[float] = state.get("budget")

    if not products or budget is None:
        return {"optimized_products": []}

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    items_summary = []
    for prod in products:
        item = prod.get("item")
        category = prod.get("category")
        options = prod.get("options", [])
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
        f"Given a list of items with several product options and a total budget of ${budget}, "
        "select the best combination of products so the total price does not exceed the budget. "
        "Consider both price and rating. Try to select one option per item. "
        "If the budget is too low, you can drop items. "
        "Respond ONLY as a JSON array of the selected product objects. "
        "Example: [{\"item\": \"milk\", \"name\": \"Great Value Milk\", \"price\": 3.5, ...}]\n\n"
        f"Items and options: {items_summary}"
    )

    response = llm.invoke([{"role": "user", "content": prompt}])

    try:
        content = response.content.strip()
        if content.startswith('```json'):
            content = content[7:-3].strip()
        optimized_products = json.loads(content)
        if not isinstance(optimized_products, list):
            optimized_products = []
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"JSON parsing error in budget optimizer: {e}")
        optimized_products = []

    return {"optimized_products": optimized_products}
