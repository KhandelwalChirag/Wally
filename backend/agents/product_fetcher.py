from langchain_google_genai import ChatGoogleGenerativeAI
from states import OverallState
from typing import Dict, Any, List, Literal
from langgraph.types import Command
import asyncio
from mcp.mcp_tools import get_mcp_tools

def product_search_agent(state: OverallState) -> Command[Literal["budget_optimizer_agent"]]:
    categories = state.get("categories", {})
    products = []

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    async def fetch_products():
        tools = await get_mcp_tools()
        getProductInfo = tools["getProductInfo"]
        for item, category in categories.items():
            prompt = (
                f"You are a Walmart.com shopping assistant. "
                f"Given the item '{item}' and its category '{category}', "
                f"generate a concise search query suitable for Walmart's product search API. "
                f"Respond ONLY with the search query string."
            )
            response = llm.invoke([{"role": "user", "content": prompt}])
            search_query = response.content.strip() if hasattr(response, "content") else item

            options = await getProductInfo.ainvoke({"search_query": search_query, "category": category})
            products.append({
                "item": item,
                "options": options
            })
        return products

    products_result = asyncio.run(fetch_products())
    return Command(update={"products": products_result}, goto="budget_optimizer_agent")