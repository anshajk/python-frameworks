from dotenv import load_dotenv
from agent_framework import Agent, tool
from agent_framework.anthropic import AnthropicClient
import asyncio
from typing import Annotated
from random import randint


load_dotenv()


@tool(approval_mode="never_require")
def get_weather(
    location: Annotated[str, "The location to get the weather for."],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."


@tool(approval_mode="never_require")
def calculate_compound_interest(
    principal: Annotated[float, "The initial amount of money."],
    rate: Annotated[float, "The annual interest rate as a percentage."],
    time: Annotated[float, "The time period in years."],
    compounds_per_year: Annotated[
        int, "The number of times interest is compounded per year."
    ] = 12,
) -> str:
    """Calculate compound interest."""
    amount = principal * (1 + rate / 100 / compounds_per_year) ** (
        compounds_per_year * time
    )
    interest = amount - principal
    return f"Principal: ${principal:.2f}, Interest earned: ${interest:.2f}, Total amount: ${amount:.2f}"


async def streaming_run() -> None:
    """Example of streaming response (get results as they are generated)."""
    print("=== Streaming Response Example ===")

    agent = Agent(
        client=AnthropicClient(model="claude-sonnet-4-5-20250929"),
        name="Question Answering Agent",
        instructions="You are a helpful agent.",
        tools=[get_weather, calculate_compound_interest],
    )

    query = input("Ask the agent a question: ")
    print(f"User: {query}")
    print("Agent: ", end="", flush=True)
    async for chunk in agent.run(query, stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print("\n")


async def main() -> None:
    print("=== Anthropic Example ===")

    await streaming_run()


if __name__ == "__main__":
    asyncio.run(main())
