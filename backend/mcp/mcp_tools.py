from langchain_mcp_adapters.client import MultiServerMCPClient
import os

async def get_mcp_tools():
    client = MultiServerMCPClient(
        {
            "walmart": {
                "command": "python",
                "args": [os.path.abspath("backend/mcp/server.py")],
                "transport": "stdio",
            }
        }
    )
    tools = await client.get_tools()
    return tools