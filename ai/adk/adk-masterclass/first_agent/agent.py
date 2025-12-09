# agent.py
import logging
from google.adk.agents import Agent
from google.genai import types

# Configure logging to see what's happening under the hood
# This is crucial for debugging LLM reasoning later.
logging.basicConfig(level=logging.INFO)

# Define the Agent
# We use Gemini 2.5 Flash because it is fast and cheap for development.
coding_buddy = Agent(
    model="gemini-2.5-flash",
    name="coding_buddy",  # This ID is used for routing and logs
    instruction="""
    You are a senior software engineer assistant.
    Your goal is to help developers write clean, efficient Python code.
    
    Guidelines:
    - Always assume the user is using Python 3.10+.
    - Prefer using Type Hints in all code snippets.
    - Keep explanations concise; developers want code, not essays.
    - If you are unsure, ask clarifying questions.
    """,
    description="A helper agent for Python development tasks."
)

root_agent = coding_buddy