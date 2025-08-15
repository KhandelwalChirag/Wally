from langgraph.graph import StateGraph, START, END
from agents.states import (
    InputInterpreterInputState,
    InputInterpreterOutputState,
    OverallState,
)
from agents.input_interpreter import input_interpreter
from agents.item_extractor import item_expansion_agent
from agents.category_assigner import category_inference_agent
from agents.product_fetcher import product_search_agent
from agents.budget_optimizer import budget_optimizer_agent
from agents.cart_builder import cart_builder_agent

# Build the graph with input and output schemas specified
builder = StateGraph(
    OverallState,
    input_schema=InputInterpreterInputState,
    output_schema=InputInterpreterOutputState,
)

# Add agent nodes
builder.add_node("input_interpreter", input_interpreter)
builder.add_node("item_expansion_agent", item_expansion_agent)
builder.add_node("category_inference_agent", category_inference_agent)
builder.add_node("product_search_agent", product_search_agent)
builder.add_node("budget_optimizer_agent", budget_optimizer_agent)
builder.add_node("cart_builder_agent", cart_builder_agent)

# Edges
builder.add_edge(START, "input_interpreter")

# Conditional routing after input_interpreter
def route_after_input_interpreter(state: OverallState):
    if state.get("task_type") == "goal_or_dish":
        return "item_expansion_agent"
    else:
        return "category_inference_agent"

builder.add_conditional_edges("input_interpreter", route_after_input_interpreter)

# Add the missing sequential edges
builder.add_edge("item_expansion_agent", "category_inference_agent")
builder.add_edge("category_inference_agent", "product_search_agent")
builder.add_edge("product_search_agent", "budget_optimizer_agent")
builder.add_edge("budget_optimizer_agent", "cart_builder_agent")
builder.add_edge("cart_builder_agent", END)

graph = builder.compile()

# Example invocation
# result = graph.invoke({"user_input": "I want to make pasta for $20"})
# print(result)
