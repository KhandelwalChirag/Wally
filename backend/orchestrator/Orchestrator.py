from langgraph_supervisor import create_supervisor
from langchain_google_genai import ChatGoogleGenerativeAI
from agents.Recipe_agent import recipe_agent


supervisor = create_supervisor(
    agents = [recipe_agent],
    model = ChatGoogleGenerativeAI(model = "gemini-2.0-flash")
    tools = [],
    prompt = (""),


).compile()