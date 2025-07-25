import datetime

from zoneinfo import ZoneInfo
from google.adk.agents import Agent

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from mcp import StdioServerParameters


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degree celsius"
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for {city} is not available",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (f"Sorry, I don't have timezone information for {city}."),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    return {"status": "success", "report": report}


mcp_tool = MCPToolset(
    connection_params=StdioServerParameters(
        command="/Users/art/Projects/python-frameworks/.venv/bin/python3",
        args=["/Users/art/Projects/python-frameworks/ai/fastmcp/server.py"],
    )
)

root_agent = Agent(
    name="IK_Weather_agent",
    model="gemini-2.0-flash",
    description=("Agent to answer questions about the time and weather in a city"),
    tools=[get_weather, get_current_time, mcp_tool],
)
