"""Batching several questions against one shared input.

Independent questions belong in the same request: they share the input tokens
(which is all you pay for) and are evaluated together.

Dependent questions do not. If question B only makes sense given the answer to
A, you need two round trips -- a single request cannot branch. The second half
of this demo shows that sequencing.

Run:
    python multi_question_demo.py
"""

from _common import MODEL, decision_cost, get_client, print_usage, require

REVIEW = (
    "Shipping took three weeks and the box arrived crushed, but honestly the "
    "headphones themselves sound incredible and the battery lasts for days. "
    "Support never replied to my two emails about the delay."
)

BATCH = [
    {
        "type": "predicate",
        "name": "mentions_shipping",
        "instructions": "Does the review mention shipping, delivery, or packaging?",
    },
    {
        "type": "predicate",
        "name": "needs_followup",
        "instructions": "Does the reviewer describe an unresolved problem that support should follow up on?",
    },
    {
        "type": "choice",
        "name": "primary_topic",
        "instructions": "What is the review mostly about?",
        "choices": [
            {"value": "product_quality", "description": "The item itself: sound, build, battery."},
            {"value": "logistics", "description": "Shipping, delivery times, packaging."},
            {"value": "support", "description": "Interactions with customer service."},
            {"value": "other", "description": "Anything else."},
        ],
    },
    {
        "type": "score",
        "name": "satisfaction",
        "instructions": "How satisfied is the reviewer overall?",
        "levels": [
            {"label": "Angry", "description": "Actively upset, likely to churn."},
            {"label": "Mixed", "description": "Real complaints alongside real praise."},
            {"label": "Delighted", "description": "Overwhelmingly positive."},
        ],
    },
]


def batched(client) -> None:
    print("One request, four independent questions\n")
    decision = client.decisions.create(model=MODEL, input=REVIEW, questions=BATCH)

    for answer in decision.answers:
        if answer.type == "refusal":
            print(f"  {answer.name:<18} REFUSED")
        elif answer.type == "predicate":
            print(f"  {answer.name:<18} p={answer.probability:.2f}")
        elif answer.type == "choice":
            print(f"  {answer.name:<18} {answer.choice} (confidence {answer.confidence:.2f})")
        elif answer.type == "score":
            print(f"  {answer.name:<18} {answer.score:.2f} (confidence {answer.confidence:.2f})")

    print_usage(decision)
    return decision


def sequenced(client) -> None:
    """Question two depends on question one, so it needs its own request."""
    print("\nTwo requests, because the second question depends on the first\n")

    first = client.decisions.create(
        model=MODEL,
        input=REVIEW,
        questions=[
            {
                "type": "predicate",
                "name": "needs_followup",
                "instructions": "Does the reviewer describe an unresolved problem that support should follow up on?",
            }
        ],
    )
    followup = require(first, "needs_followup")
    print(f"  step 1: needs_followup p={followup.probability:.2f}")

    if followup.probability < 0.5:
        print("  step 2: skipped, nothing to route")
        return

    second = client.decisions.create(
        model=MODEL,
        input=REVIEW,
        questions=[
            {
                "type": "choice",
                "name": "followup_owner",
                "instructions": "Which team should own the follow-up for this unresolved problem?",
                "choices": [
                    {"value": "logistics", "description": "Carrier claims and re-shipment."},
                    {"value": "support", "description": "Replying to the customer directly."},
                    {"value": "refunds", "description": "Issuing money back."},
                    {"value": "other", "description": "Anything else."},
                ],
            }
        ],
    )
    owner = require(second, "followup_owner")
    print(f"  step 2: followup_owner = {owner.choice} (confidence {owner.confidence:.2f})")
    print(f"\n  sequenced total cost: ${decision_cost(first) + decision_cost(second):.8f}")
    print("  (the review's input tokens were paid for twice)")


def main() -> None:
    client = get_client()
    batched(client)
    sequenced(client)


if __name__ == "__main__":
    main()
