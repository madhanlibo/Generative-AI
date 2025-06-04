from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calender Assistant")

@mcp.tool()
def get_event(day:str)->str:
    return f"Ther is no event on {day}"

@mcp.tool()
def get_anniversary_this_week() -> str:
    return "It is your marriage anniversary tomorrow"

if __name__ == "__main__":
    mcp.run(transport="sse")