from langchain_google_genai import ChatGoogleGenerativeAI
from states import InputInterpreterInputState
from typing import Literal
from langgraph.types import Command

from dotenv import load_dotenv

load_dotenv()

def input_interpreter(state: InputInterpreterInputState) -> Command[Literal["item_expansion_agent", "category_inference_agent"]]:
    user_input = state.get("user_input", "")

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    prompt = (
        "You are a highly skilled AI assistant for a smart shopping cart system. "
        "Your job is to analyze the user's input and extract the following information:\n\n"
        "1. task_type: Determine if the input is a direct product list (the user lists specific products to buy) "
        "or a goal/dish/task (the user describes a dish to make, a meal to prepare, or a shopping goal). "
        "Return 'direct_product_list' or 'goal_or_dish'.\n"
        "2. item_list: Return a list of product names if the user listed products, or a list with the dish/goal name if the input is goal/dish-based.\n"
        "3. budget: Extract the budget as a float if the user mentions a budget (e.g., '$50', 'under 100 dollars'). If no budget is mentioned, return null.\n\n"
        "Respond ONLY as a JSON object with the following keys: task_type, item_list, budget.\n"
        "Do not include any explanation or extra text. Example:\n"
        "{\n"
        '  "task_type": "direct_product_list",\n'
        '  "item_list": ["milk", "bread", "eggs"],\n'
        '  "budget": 25.0\n'
        "}\n\n"
        "User input: " + user_input
    )

    response = llm.invoke([{"role": "user", "content": prompt}])

    try:
        import json
        content = response.content.strip()
        # Remove markdown code block markers if present
        if content.startswith('```json'):
            content = content[7:]
        if content.endswith('```'):
            content = content[:-3]
        parsed = json.loads(content.strip())
        task_type = parsed.get("task_type")
        item_list = parsed.get("item_list", [])
        budget = parsed.get("budget")
    except Exception:
        task_type = None
        item_list = []
        budget = None

    update = {
        "task_type": task_type,
        "item_list": item_list,
        "budget": budget,
    }
    if task_type == "goal_or_dish":
        return Command(update=update, goto="item_expansion_agent")
    else:
        return Command(update=update, goto="category_inference_agent")