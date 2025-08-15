from langgraph.graph import StateGraph, START, END
from database import get_postgres_checkpointer

import getpass
import os
import uuid
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
if "DATABASE_URL" not in os.environ:
    os.environ["DATABASE_URL"] = "postgresql://postgres:password@localhost:5432/smart_cart_db"

from states import (
    InputInterpreterInputState,
    InputInterpreterOutputState,
    OverallState,
)
from input_interpreter import input_interpreter
from item_extractor import item_expansion_agent
from category_assigner import category_inference_agent
from product_fetcher import product_search_agent
from budget_optimizer import budget_optimizer_agent
from cart_builder import cart_builder_agent

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

# Create PostgreSQL checkpointer for saving graph state
checkpointer = get_postgres_checkpointer()

# Update graph compilation to use the checkpointer
graph = builder.compile(checkpointer=checkpointer)

# Visualize the compiled graph
try:
    from IPython.display import Image, display
    display(Image(graph.get_graph().draw_mermaid_png()))
except ImportError:
    print("IPython not available. Install with: pip install ipython")
except Exception as e:
    print(f"Graph visualization failed: {e}")

# Example usage:
result = graph.invoke({"user_input": "I want to make pasta for $20"})