"""Microsoft Agent Framework example: the handoff (dynamic routing) pattern.

``HandoffBuilder`` lets agents transfer control among themselves at runtime. A triage
agent starts every conversation and hands off to the right specialist based on the
request — the routing decision is made by the model, not hard-coded edges.

Run it:

    export OPENAI_API_KEY=...
    python ai/multi_agent/agent_framework/triage_handoff.py
"""

import asyncio
import os

from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import HandoffBuilder

MODEL = "gpt-4o-mini"


def build_agents() -> tuple[Agent, Agent, Agent]:
    client = OpenAIChatClient(model=MODEL, api_key=os.environ["OPENAI_API_KEY"])
    # Handoff workflows require this flag so each agent's local history stays consistent
    # with the service across the handoff tool-call short-circuits.
    triage = Agent(
        client=client,
        name="Triage",
        instructions="You are a support triage agent. Briefly greet the user, then hand "
        "off to the specialist that best fits their request. Do not solve it yourself.",
        require_per_service_call_history_persistence=True,
    )
    billing = Agent(
        client=client,
        name="Billing",
        instructions="You are a billing specialist. Resolve invoice, refund, and "
        "subscription questions clearly.",
        require_per_service_call_history_persistence=True,
    )
    technical = Agent(
        client=client,
        name="Technical",
        instructions="You are a technical specialist. Resolve errors and how-to "
        "questions with concrete steps.",
        require_per_service_call_history_persistence=True,
    )
    return triage, billing, technical


async def main() -> None:
    triage, billing, technical = build_agents()
    workflow = (
        HandoffBuilder(participants=[triage, billing, technical])
        .with_start_agent(triage)
        .add_handoff(triage, [billing, technical])
        .build()
    )
    result = await workflow.run("I was charged twice for my subscription this month.")
    for output in result.get_outputs():
        print(output)


if __name__ == "__main__":
    asyncio.run(main())
