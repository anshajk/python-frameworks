"""The golden dataset for the support-triage agent.

Each case captures the three things a good agent test needs:

* ``input``            - the user's query,
* ``expected_tools``   - which tools *should* be called (this is how we grade the journey),
* ``reference_answer`` - a ground-truth answer the judge compares against (the destination).

Kept intentionally small but representative: policy question, account lookup, a case that
needs both tools, and an edge case (unknown account). Hand-curated cases like these are
worth far more than a thousand random ones.
"""

from typing import Any, Dict, List

GOLDEN_DATASET: List[Dict[str, Any]] = [
    {
        "input": "How do I reset my password?",
        "expected_tools": ["search_knowledge_base"],
        "reference_answer": (
            "Open Settings > Security > Reset Password. You'll get an emailed reset "
            "link that expires after one hour."
        ),
    },
    {
        "input": "What plan is account A-1001 on and how many seats does it have?",
        "expected_tools": ["get_subscription"],
        "reference_answer": "Account A-1001 is on the annual plan with 5 seats.",
    },
    {
        "input": "I'm on account A-2002 — am I eligible for a refund?",
        "expected_tools": ["get_subscription", "search_knowledge_base"],
        "reference_answer": (
            "Account A-2002 is on a monthly plan, which is non-refundable, though it "
            "can be cancelled anytime."
        ),
    },
    {
        "input": "Can you look up the plan for account A-9999?",
        "expected_tools": ["get_subscription"],
        "reference_answer": (
            "There's no account A-9999 on file, so the plan can't be looked up."
        ),
    },
]
