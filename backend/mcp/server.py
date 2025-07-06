from fastmcp import FastMCP

mcp = FastMCP("Walmart_Datafetch_server")

@mcp.tool
def getProductInfo():
    return ""

if __name__ == "__main__":
    mcp.run(port=5000,transport = "streamable-http")