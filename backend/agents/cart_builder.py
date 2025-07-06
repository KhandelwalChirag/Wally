from states import OverallState
from typing import Dict, Any, List, Literal
from langgraph.types import Command
import asyncio
from mcp.mcp_tools import get_mcp_tools

def cart_builder_agent(state: OverallState) -> Command[Literal["END"]]:
    optimized_products: List[Dict[str, Any]] = state.get("optimized_products", [])
    if not optimized_products:
        return Command(update={"cart_url": ""}, goto="END")

    async def build_cart():
        tools = await get_mcp_tools()
        buildCartUrl = tools["buildCartUrl"]
        cart_url = await buildCartUrl.ainvoke({"products": optimized_products})
        return cart_url

    cart_url = asyncio.run(build_cart())
    return Command(update={"cart_url": cart_url}, goto="END")