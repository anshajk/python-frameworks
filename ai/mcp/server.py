# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("DemoServer")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


@mcp.prompt("greet_user")
def greet_user(name: str) -> str:
    """Generate a greeting message for the user"""
    return f"Welcome to the MCP server, {name}!"
