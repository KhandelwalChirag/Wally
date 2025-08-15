from langchain_google_genai import ChatGoogleGenerativeAI
from states import OverallState
from typing import Literal
from langgraph.types import Command
from dotenv import load_dotenv

load_dotenv()
def item_expansion_agent(state: OverallState) -> Command[Literal["category_inference_agent"]]:
    """
    Expands a high-level goal/dish/task into a flat list of specific product needs.
    Only called if state["task_type"] == "goal_or_dish".
    """

    item_list = state.get("item_list", [])
    if not item_list:
        return Command(update={"expanded_items": []}, goto="category_inference_agent")

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    # Assume only one goal/dish per input for simplicity
    goal = item_list[0] if isinstance(item_list, list) and item_list else ""
    prompt = (
        "You are an expert assistant. Given a user's goal/ problem or dish, "
        "expand it into a flat list of specific items.(ingredients and tools if needed). "
        "Return ONLY a JSON array of item names. No extra text.\n\n"
        f"Goal or dish: {goal}\n"
        "Example response:\n"
        '["spaghetti", "tomato sauce", "ground beef", "onion", "garlic"]'
    )

    response = llm.invoke([{"role": "user", "content": prompt}])

    try:
        import json
        expanded_items = response.content if isinstance(response.content, list) else response.content.strip()
        if isinstance(expanded_items, str):
            expanded_items = json.loads(expanded_items)
        if not isinstance(expanded_items, list):
            expanded_items = []
    except Exception:
        expanded_items = []

    return Command(update={"expanded_items": expanded_items}, goto="category_inference_agent")
