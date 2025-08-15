from langchain_google_genai import ChatGoogleGenerativeAI
from agents.states import OverallState
from typing import Dict, Any
import json
from dotenv import load_dotenv

load_dotenv()

def item_expansion_agent(state: OverallState) -> Dict[str, Any]:
    """
    Expands a high-level goal into a list of specific items.
    Returns a dictionary with the 'expanded_items' update.
    """
    item_list = state.get("item_list", [])
    if not item_list or state.get("task_type") != "goal_or_dish":
        return {"expanded_items": []}

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    goal = item_list[0] if isinstance(item_list, list) and item_list else ""
    prompt = (
        "You are an expert assistant. Given a user's goal or dish, "
        "expand it into a flat list of specific items (ingredients and tools if needed). "
        "Return ONLY a JSON array of item names. No extra text.\n\n"
        f"Goal or dish: {goal}\n"
        'Example response: ["spaghetti", "tomato sauce", "ground beef", "onion", "garlic"]'
    )

    response = llm.invoke([{"role": "user", "content": prompt}])

    try:
        content = response.content.strip()
        if content.startswith('```json'):
            content = content[7:-3].strip()
        expanded_items = json.loads(content)
        if not isinstance(expanded_items, list):
            expanded_items = []
    except (json.JSONDecodeError, AttributeError):
        expanded_items = []

    return {"expanded_items": expanded_items}
