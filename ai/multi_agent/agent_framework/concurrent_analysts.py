"""Microsoft Agent Framework example: the concurrent (fan-out/fan-in) pattern.

``ConcurrentBuilder`` wires a dispatcher -> fan-out -> participants -> fan-in ->
aggregator graph for you. Here three analyst agents evaluate the same prompt from
different stances *in parallel*, and a custom aggregator merges their takes into one
brief. This is the multi-agent sweet spot: independent work that runs simultaneously.

Run it:

    export OPENAI_API_KEY=...
    python ai/multi_agent/agent_framework/concurrent_analysts.py
"""

import asyncio
import os

from agent_framework import Agent, AgentExecutorResponse
from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import ConcurrentBuilder

MODEL = "gpt-4o-mini"


def build_client() -> OpenAIChatClient:
    return OpenAIChatClient(model=MODEL, api_key=os.environ["OPENAI_API_KEY"])


def make_analysts() -> list[Agent]:
    client = build_client()
    return [
        Agent(
            client=client,
            name="BullAnalyst",
            instructions="You are an optimistic analyst. Argue the strongest bull case "
            "for the proposal in 3 concise bullet points.",
        ),
        Agent(
            client=client,
            name="BearAnalyst",
            instructions="You are a skeptical analyst. Argue the strongest bear case "
            "against the proposal in 3 concise bullet points.",
        ),
        Agent(
            client=client,
            name="RiskAnalyst",
            instructions="You are a risk analyst. List the top 3 risks and how to "
            "mitigate each, concisely.",
        ),
    ]


def merge(results: list[AgentExecutorResponse]) -> str:
    """Fan-in: combine each analyst's final message into one brief."""
    sections = [
        f"## {r.agent_response.agent_name or 'Analyst'}\n"
        f"{r.agent_response.messages[-1].text}"
        for r in results
    ]
    return "\n\n".join(sections)


async def main() -> None:
    workflow = (
        ConcurrentBuilder(participants=make_analysts()).with_aggregator(merge).build()
    )
    result = await workflow.run(
        "Should we launch a solar-powered edge camera product line next year?"
    )
    for output in result.get_outputs():
        print(output)


if __name__ == "__main__":
    asyncio.run(main())
