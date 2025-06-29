from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langain_tavily import TavilySearch
from pydantic import BaseModel

#search tool for combining online available recipies of Dishes


search_tool = TavilySearch(
    max_results = 5,
    topic = "Food recepies"
)

recipe_agent = create_react_agent(
    model = ChatGoogleGenerativeAI(model = "gemini-2.0-flash"),
    tools = [search_tool],
    prompt = ""
)