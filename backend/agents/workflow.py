from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt
from agents.states import (
    InputInterpreterInputState,
    InputInterpreterOutputState,
    OverallState,
)

from langgraph.checkpoint.memory import InMemorySaver

from agents.input_interpreter import input_interpreter
from agents.item_extractor import item_expansion_agent
from agents.category_assigner import category_inference_agent
from agents.product_fetcher import product_search_agent
from agents.budget_optimizer import budget_optimizer_agent
from agents.cart_builder import cart_builder_agent


def human_verification(state: OverallState) -> OverallState:
    """
    Pauses the graph to allow a human to review and edit the item list.
    This node will loop, re-prompting the user until they 'accept' the list.
    """
    current_list = state["item_list"]
    while True:
        user_feedback = interrupt({
            "task": "Please review the item list. You can 'accept' it or 'edit' it.",
            "current_list": current_list
        })

        action = user_feedback.get("action")

        if action == "accept":
            print("--- User accepted the list. Continuing graph execution. ---")
            return {"item_list": current_list}
        elif action == "edit":
            new_list = user_feedback.get("editedList")
            if new_list is not None:
                print(f"--- User edited the list. New list: {new_list} ---")
                current_list = new_list
            else:
                print("--- 'edit' action received without a new list. Re-prompting. ---")
        else:
            print(f"--- Invalid action '{action}' received. Re-prompting. ---")



builder = StateGraph(
    OverallState,
    input_schema=InputInterpreterInputState,
    output_schema=InputInterpreterOutputState,
)

builder.add_node("input_interpreter", input_interpreter)
builder.add_node("item_expansion_agent", item_expansion_agent)
builder.add_node("category_inference_agent", category_inference_agent)
builder.add_node("product_search_agent", product_search_agent)
builder.add_node("budget_optimizer_agent", budget_optimizer_agent)
builder.add_node("cart_builder_agent", cart_builder_agent)
builder.add_node("Human_review", human_verification)

builder.add_edge(START, "input_interpreter")

def route_after_input_interpreter(state: OverallState):
    if state.get("task_type") == "goal_or_dish":
        return "item_expansion_agent"
    else:
        return "category_inference_agent"

builder.add_conditional_edges("input_interpreter", route_after_input_interpreter)
builder.add_edge("item_expansion_agent", "Human_review")
builder.add_edge("Human_review", "category_inference_agent")
builder.add_edge("category_inference_agent", "product_search_agent")
builder.add_edge("product_search_agent", "budget_optimizer_agent")
builder.add_edge("budget_optimizer_agent", END)

# builder.add_edge("budget_optimizer_agent", "cart_builder_agent")
# builder.add_edge("cart_builder_agent", END)

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)
