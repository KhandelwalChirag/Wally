from states import OverallState
from langgraph.types import Command

def cart_builder_agent(state: OverallState) -> Command:
    products = state.get("optimized_products", [])
    if not products:
        return Command(update={"cart_url": ""}, goto="END")

    return Command(
        call="buildCartUrl",
        args={"products": products},
        update_to="cart_url",
        goto="END"
    )
