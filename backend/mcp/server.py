from fastmcp import FastMCP

mcp = FastMCP("Walmart_Datafetch_server")

@mcp.tool
def getProductInfo():
    return ""