"""Predicate questions: calibrated yes/no probabilities.

A predicate returns `probability`, not a boolean. The threshold is your
decision, not the model's -- see threshold_tuning_demo.py for picking one.

Image predicates live in image_predicate_demo.py, which measures them against
a real labelled photo dataset.

Run:
    python predicate_demo.py
"""

from _common import MODEL, get_client, print_usage, require

REVIEW_THRESHOLD = 0.80

PASSAGES = [
    "Refunds are issued to the original payment method within 5-10 business days.",
    "Our offices will be closed on November 24th for the holiday.",
    "To reset your password, click 'Forgot password' on the sign-in screen.",
]

QUESTION = (
    "Does this passage help answer the question "
    "'How long does a refund take to arrive?' "
    "Judge only whether it contains relevant information, not whether it is complete."
)


def check_relevance(client) -> None:
    print(f"Question: how long does a refund take?\n(flagging at p >= {REVIEW_THRESHOLD})\n")
    for passage in PASSAGES:
        decision = client.decisions.create(
            model=MODEL,
            input=passage,
            questions=[
                {"type": "predicate", "name": "is_relevant", "instructions": QUESTION}
            ],
        )
        answer = require(decision, "is_relevant")
        verdict = "RELEVANT" if answer.probability >= REVIEW_THRESHOLD else "skip"
        print(f"  p={answer.probability:.2f}  {verdict:<9} {passage[:60]}")
        print_usage(decision)


def main() -> None:
    client = get_client()
    check_relevance(client)


if __name__ == "__main__":
    main()
