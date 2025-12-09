# agent_with_tools.py
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

# Import the functions we defined above
from .tools import get_weather_report, analyze_sentiment

weather_bot = Agent(
    model="gemini-2.5-flash",
    name="weather_bot",
    # We pass the raw functions; ADK wraps them in FunctionTool automatically
    tools=[get_weather_report, analyze_sentiment],
    instruction="""
    You are a helpful weather assistant.
    
    Execution Logic:
    1. If the user asks for weather, call `get_weather_report`.
    2. CHECK the 'status' field in the return value.
       - If 'success': Present the weather in a friendly way.
       - If 'error': Apologize and explicitly suggest checking "London" or "Paris".
    3. If the user replies with an opinion (e.g., "I hate rain"), call `analyze_sentiment`.
       - Respond with empathy based on the sentiment score.
    """,
)


root_agent = weather_bot
