"""ADK multi-agent example: LLM-driven delegation (coordinator + specialists).

Unlike the deterministic workflow agents (Sequential/Parallel/Loop), this pattern lets
the *model* decide routing at runtime. A coordinator ``LlmAgent`` is given specialist
``sub_agents``; based on the user's request it transfers control to whichever specialist
fits. This is ADK's hierarchical / handoff pattern.

The coordinator delegates by generating a ``transfer_to_agent`` action, which ADK routes
to the named sub-agent — no hard-coded edges required.

Run it:

    export GOOGLE_API_KEY=...
    adk run ai/multi_agent/adk/support_coordinator
"""

from google.adk.agents import LlmAgent

GEMINI_MODEL = "gemini-2.0-flash"

billing_agent = LlmAgent(
    name="BillingAgent",
    model=GEMINI_MODEL,
    description="Handles billing, invoices, refunds, and subscription questions.",
    instruction=(
        "You are a billing specialist. Answer questions about invoices, refunds, plans, "
        "and payments clearly and empathetically. Stay strictly within billing."
    ),
)

technical_agent = LlmAgent(
    name="TechnicalAgent",
    model=GEMINI_MODEL,
    description="Handles technical troubleshooting, errors, setup, and how-to questions.",
    instruction=(
        "You are a technical support specialist. Help diagnose errors, setup issues, and "
        "how-to questions with concrete, step-by-step guidance. Stay strictly technical."
    ),
)

# The coordinator does not answer directly — it routes to the right specialist. ADK
# turns this into a transfer_to_agent handoff based on the sub_agents' descriptions.
root_agent = LlmAgent(
    name="SupportCoordinator",
    model=GEMINI_MODEL,
    description="Front-line coordinator that routes requests to a specialist.",
    instruction=(
        "You are a support triage coordinator. Do not answer questions yourself. "
        "Inspect the user's request and delegate to exactly one specialist: transfer to "
        "BillingAgent for billing/payment/refund topics, or TechnicalAgent for technical "
        "troubleshooting and how-to topics. If it is neither, ask a clarifying question."
    ),
    sub_agents=[billing_agent, technical_agent],
)
