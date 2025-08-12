from langgraph.graph import StateGraph, START, END

import getpass
import os
from dotenv import load_dotenv
try:
    from IPython.display import Image, display
except ImportError:
    pass

load_dotenv()
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")
if "TAVILY_API_KEY" not in os.environ:
    os.environ["TAVILY_API_KEY"] = getpass.getpass("Enter your Tavily API key: ")

from .states import (
    InputInterpreterInputState,
    InputInterpreterOutputState,
    OverallState,
)
from .input_interpreter import input_interpreter
from .item_extractor import item_expansion_agent
from .category_assigner import category_inference_agent
from .product_fetcher import product_search_agent
from .budget_optimizer import budget_optimizer_agent
from .cart_builder import cart_builder_agent

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
builder.add_edge("cart_builder_agent", END)

# All other transitions are handled by Command-based handoffs in the agent nodes

graph = builder.compile()

