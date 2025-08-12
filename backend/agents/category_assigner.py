from langchain_google_genai import ChatGoogleGenerativeAI
from .states import OverallState
from typing import Dict, Any, List, Literal
from langgraph.types import Command, interrupt
from dotenv import load_dotenv

load_dotenv()

def category_inference_agent(state: OverallState) -> Command[Literal["product_search_agent"]]:
    """
    Maps each item to a Walmart category name using LLM reasoning.
    Returns: {"categories": {item: category_name, ...}}
    """
    # Use expanded_items if present, else item_list
    
    items: List[str] = state.get("expanded_items") or state.get("item_list") or []
    print(f"Category inference received items: {items}")
    if not items:
        print("No items found, returning empty categories")
        return Command(update={"categories": {}}, goto="product_search_agent")

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    prompt = (
        "You are a Walmart.com shopping assistant. "
        "Given a list of product names, map each to the most relevant Walmart.com category name. "
        "Use only top-level or second-level categories as found on Walmart.com. "
        "Respond ONLY as a JSON object mapping each item to its category name. "
        "Example:\n"
        '{\n'
        '  "milk": "Dairy & Eggs",\n'
        '  "spaghetti": "Pasta & Noodles",\n'
        '  "tomato sauce": "Pantry"\n'
        '}\n\n'
        f"Items: {items}"
    )

    response = llm.invoke([{"role": "user", "content": prompt}])

    try:
        import json
        content = response.content.strip()

        if content.startswith('```json'):
            content = content[7:]  
        if content.endswith('```'):
            content = content[:-3] 
        content = content.strip()
        categories = json.loads(content)
        if not isinstance(categories, dict):
            categories = {}
    except Exception as e:
        print(f"JSON parsing error: {e}")
        categories = {}

    print(f"Category inference result: {categories}")
    
    # Add human review interrupt
    if items:
        categories = interrupt({
            "type": "category_review",
            "items": items,
            "suggested_categories": categories,
            "message": "Please review the category assignments for these items."
        })
    
    return Command(update={"categories": categories, "interrupt_type": "category_review"}, goto="product_search_agent")

