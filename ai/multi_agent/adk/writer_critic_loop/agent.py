"""ADK multi-agent example: the reflection (loop) pattern.

A ``LoopAgent`` runs a writer and a critic in a cycle: the writer drafts (or revises
using the previous critique), the critic evaluates the draft, and the loop repeats until
the critic is satisfied or the iteration budget is hit.

Termination is handled two ways, which is the important lesson of this pattern:

* a hard cap via ``max_iterations`` (so it can never spin forever), and
* an early exit when the critic calls the ``exit_loop`` tool, which sets
  ``escalate = True`` to break out of the loop.

Run it:

    export GOOGLE_API_KEY=...
    adk run ai/multi_agent/adk/writer_critic_loop
"""

from google.adk.agents import LlmAgent, LoopAgent
from google.adk.tools import ToolContext

GEMINI_MODEL = "gemini-2.0-flash"


def exit_loop(tool_context: ToolContext) -> dict:
    """Signal that the draft is good enough and the refinement loop should stop."""
    tool_context.actions.escalate = True
    return {"status": "approved", "message": "Draft approved; exiting refinement loop."}


# The '?' makes {critique} optional, so the first iteration (no critique yet) works.
writer = LlmAgent(
    name="Writer",
    model=GEMINI_MODEL,
    description="Writes or revises a short piece based on critic feedback.",
    instruction=(
        "You are a writer. Write a concise paragraph on the user's topic.\n"
        "If review feedback is present below, revise your previous draft to address "
        "every point in it. Otherwise, write a strong first draft.\n\n"
        "Previous feedback (may be empty):\n{critique?}"
    ),
    output_key="draft",
)

critic = LlmAgent(
    name="Critic",
    model=GEMINI_MODEL,
    description="Critiques the draft or approves it to end the loop.",
    instruction=(
        "You are a demanding editor reviewing the draft below.\n\n"
        "Draft:\n{draft}\n\n"
        "If the draft is clear, accurate, and well-structured, call the `exit_loop` "
        "tool and say nothing else. Otherwise, do NOT call the tool; instead return a "
        "short, specific list of concrete improvements the writer should make."
    ),
    tools=[exit_loop],
    output_key="critique",
)

root_agent = LoopAgent(
    name="WriterCriticLoop",
    sub_agents=[writer, critic],
    description="Iteratively drafts and critiques until approved or the cap is reached.",
    max_iterations=3,
)
