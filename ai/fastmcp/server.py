from fastmcp import FastMCP, Context


mcp = FastMCP(
    name="My math server",
    instructions="This server can be used for arithmetic computation tasks",  # Instructions for LLM clients
    version="1.0.0",  # Server version
)


@mcp.tool
async def calculate_sum(a: int, b: int, context: Context) -> int:
    """Calculate the sum of two integers."""
    await context.warning(f"Adding {a} and {b}")
    return a + b


@mcp.tool
def calculate_difference(a: int, b: int) -> int:
    """Calculate the difference between two integers."""
    return a - b


@mcp.tool
async def calculate_product(a: int, b: int, context: Context) -> int:
    """Calculate the product of two integers."""
    await context.info(f"Multiplying {a} and {b}")
    return a * b


@mcp.tool
def calculate_quotient(a: int, b: int) -> float:
    """Calculate the quotient of two integers."""
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


@mcp.resource("config://version")
def get_version():
    return "2.0.1"


# Dynamic resource template
@mcp.resource("users://{user_id}/profile")
def get_profile(user_id: int):
    # Fetch profile for user_id...
    return {"name": f"User {user_id}", "status": "active"}


@mcp.tool
async def process_data(uri: str, ctx: Context):
    # Log a message to the client
    await ctx.info(f"Processing {uri}...")

    # Read a resource from the server
    data = await ctx.read_resource(uri)

    # Ask client LLM to summarize the data
    summary = await ctx.sample(f"Summarize: {data.content[:500]}")

    # Return the summary
    return summary.text


@mcp.prompt("greet_user")
def greet_user(name: str) -> str:
    """Generate a greeting message for the user"""
    return f"Welcome to the MCP server, {name}!"


@mcp.prompt("calculate_sum")
def calculate_sum(a: int, b: int) -> str:
    """Calculate the sum of two integers and return a message"""
    result = calculate_sum(a, b)
    return f"The sum of {a} and {b} is {result}."


if __name__ == "__main__":
    mcp.run()
