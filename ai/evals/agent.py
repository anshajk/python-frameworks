"""A small support-triage agent, built to be *evaluated*.

This is the agent under test in the "Evaluating Agentic Systems" article. It is
deliberately tiny: one LLM reasoning loop and two tools. What matters for evals is
that every run returns not just the final answer, but the full **trajectory** (which
tools were called, with what arguments) and the **retrieval context** the answer was
supposed to be grounded in.

Run it directly to see a single trajectory:

    export OPENAI_API_KEY=...
    python ai/evals/agent.py
"""

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List

from openai import OpenAI

MODEL = "gpt-4o-mini"

# --- Mock backends the tools read from -------------------------------------------------
# In a real system these would hit a vector DB and a billing API. For the article we keep
# them in-memory so the agent is fully reproducible and free to run.

_KNOWLEDGE_BASE: Dict[str, str] = {
    "refund": "Refunds are available within 30 days of purchase for annual plans. "
    "Monthly plans are non-refundable but can be cancelled anytime.",
    "reset password": "To reset a password, open Settings > Security > Reset Password. "
    "A reset link is emailed and expires after 1 hour.",
    "downtime": "Scheduled maintenance happens on the first Sunday of each month, "
    "02:00-04:00 UTC. Live status is at status.example.com.",
}

_ACCOUNTS: Dict[str, Dict[str, Any]] = {
    "A-1001": {"plan": "annual", "status": "active", "seats": 5},
    "A-2002": {"plan": "monthly", "status": "past_due", "seats": 1},
}


# --- Tools -----------------------------------------------------------------------------
# Following the repo convention, tools return a status dict rather than a bare value.

def search_knowledge_base(query: str) -> Dict[str, Any]:
    """Search the help-center knowledge base for articles matching a query."""
    hits = [text for key, text in _KNOWLEDGE_BASE.items() if key in query.lower()]
    if not hits:
        return {"status": "error", "error_message": "No matching articles found."}
    return {"status": "success", "documents": hits}


def get_subscription(account_id: str) -> Dict[str, Any]:
    """Look up a customer's subscription details by account id."""
    account = _ACCOUNTS.get(account_id.upper())
    if account is None:
        return {"status": "error", "error_message": f"Unknown account {account_id}."}
    return {"status": "success", "account_id": account_id.upper(), "details": account}


_TOOL_REGISTRY = {
    "search_knowledge_base": search_knowledge_base,
    "get_subscription": get_subscription,
}

_TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Search the help-center knowledge base for relevant articles.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_subscription",
            "description": "Look up a customer's subscription/plan details by account id.",
            "parameters": {
                "type": "object",
                "properties": {"account_id": {"type": "string"}},
                "required": ["account_id"],
            },
        },
    },
]

_SYSTEM_PROMPT = (
    "You are a customer-support triage agent. Use the knowledge base for how-to and "
    "policy questions, and the subscription lookup for account-specific questions. "
    "Only state facts supported by tool results. If a tool returns an error, say so "
    "plainly instead of guessing."
)


@dataclass
class AgentResult:
    """Everything an eval needs: the destination *and* the journey."""

    answer: str
    trajectory: List[Dict[str, Any]] = field(default_factory=list)
    retrieval_context: List[str] = field(default_factory=list)


def run_agent(user_query: str, max_steps: int = 4) -> AgentResult:
    """Run the agent loop and return the answer plus a full trajectory record."""
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ]
    trajectory: List[Dict[str, Any]] = []
    retrieval_context: List[str] = []

    for _ in range(max_steps):
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=_TOOL_SCHEMAS
        )
        message = response.choices[0].message
        messages.append(message.model_dump(exclude_none=True))

        if not message.tool_calls:
            return AgentResult(
                answer=message.content or "",
                trajectory=trajectory,
                retrieval_context=retrieval_context,
            )

        for call in message.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments or "{}")
            output = _TOOL_REGISTRY[name](**args)
            trajectory.append({"tool": name, "input": args, "output": output})
            if name == "search_knowledge_base" and output.get("status") == "success":
                retrieval_context.extend(output["documents"])
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(output),
                }
            )

    return AgentResult(
        answer="I couldn't complete the request within the step budget.",
        trajectory=trajectory,
        retrieval_context=retrieval_context,
    )


if __name__ == "__main__":
    result = run_agent("I'm on account A-2002, can I get a refund?")
    print("ANSWER:\n", result.answer)
    print("\nTRAJECTORY:")
    for step in result.trajectory:
        print(f"  - {step['tool']}({step['input']}) -> {step['output']}")
    print("\nRETRIEVAL CONTEXT:", result.retrieval_context)
