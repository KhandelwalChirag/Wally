from backend.agents.sharedState import SharedState
from langchain_google_genai import ChatGoogleGenerativeAI

def item_expansion_agent(state: SharedState) -> dict:
    """
    ItemExpansionAgent

    Goal:
        Expand high-level goals (e.g., “make pasta”) into a flat list of specific items (ingredients/tools).

    Tasks:
        - Use Gemini LLM to take a goal/dish/task from item_list and expand it into a list of concrete products/ingredients/tools.
        - Output: {"item_list": [expanded list of items]}

    Returns:
        Dict: with updated "item_list" (expanded).
    """

    # Use the first item in item_list as the goal/dish/task
    goal = state.get("task")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    prompt = (
        """
You are a helpful assistant that takes high-level goals and expands them into a detailed list of specific, tangible items needed to accomplish that goal. Your job is to interpret the goal, determine all necessary physical items (ingredients, tools, materials), and output them in a structured list with specific names and estimated amounts.

Instructions:

1. Understand the Goal  
   Break down the high-level goal (e.g., “make pasta” or “fix a nut that is stuck”) into its physical requirements: ingredients, tools, and materials.

2. Assume a Standard Scenario  
   Unless specified otherwise, assume the task is performed in a typical household setting.

3. Output Format  
   Provide a flat list called item_list, where each element is a dictionary of the form:

   {"name": "<item_name>", "amount": "<approximate amount or unit>"}

   Examples:
   - {"name": "olive oil", "amount": "2 tablespoons"}
   - {"name": "wrench", "amount": "1"}
   - {"name": "spaghetti", "amount": "200 grams"}

4. Be Practical and Realistic  
   Include only necessary items. Estimate reasonable quantities based on a typical use case (e.g., 1 meal for 2 people, or 1 repair job). Use standard units.

5. Include All Tools and Materials  
   Don’t just list ingredients—include tools (e.g., “saucepan”, “wrench”), utensils, or supporting materials.

6. Output Only the Python List  
   Do not add explanations, headings, or commentary—only the raw Python item_list as described.

Example Input:
"Make pasta"

Example Output:
item_list = [
    {"name": "spaghetti", "amount": "200 grams"},
    {"name": "salt", "amount": "1 tablespoon"},
    {"name": "olive oil", "amount": "2 tablespoons"},
    {"name": "garlic", "amount": "2 cloves"},
    {"name": "parmesan cheese", "amount": "50 grams"},
    {"name": "tomato sauce", "amount": "1 cup"},
    {"name": "saucepan", "amount": "1"},
    {"name": "colander", "amount": "1"},
    {"name": "stove", "amount": "1"},
    {"name": "wooden spoon", "amount": "1"},
    {"name": "knife", "amount": "1"},
    {"name": "cutting board", "amount": "1"}
]
"""
    )

    response = llm.invoke([{"role": "user", "content": prompt + goal}])
    try:
        import json
        expanded_items = response.content if isinstance(response.content, list) else response.content.strip()
        if isinstance(expanded_items, str):
            expanded_items = json.loads(expanded_items)
        if not isinstance(expanded_items, list):
            expanded_items = [goal]
    except Exception:
        expanded_items = [goal]

    return {
        "item_list": expanded_items
    }