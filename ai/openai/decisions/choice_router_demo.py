"""Choice questions: route an input to one of a fixed set of options.

Two things worth noticing in the output:
  1. The full `probabilities` distribution is more informative than `choice`.
     A 0.45/0.42 split and a 0.95/0.02 split both return a winner.
  2. The "other" fallback exists so inputs outside your taxonomy have somewhere
     to go. Without it the model must pick a wrong category.

Run:
    python choice_router_demo.py
"""

from _common import MODEL, get_client, print_distribution, print_usage, require

CONFIDENCE_FLOOR = 0.70

DEPARTMENTS = [
    {"value": "billing", "description": "Payments, invoices, refunds, and double charges."},
    {"value": "technical", "description": "Bugs, errors, and problems using the product."},
    {"value": "shipping", "description": "Delivery, tracking, and damaged parcels."},
    {"value": "other", "description": "Anything outside the categories above."},
]

TICKETS = [
    "I was charged twice for my order.",
    "The export button does nothing in Safari.",
    "My parcel says delivered but it is not here.",
    "Do you sponsor open source conferences?",
    "It broke after the payment went through and now I want my money back.",
]


def main() -> None:
    client = get_client()
    print(f"Routing {len(TICKETS)} tickets (escalating below confidence {CONFIDENCE_FLOOR})\n")

    for ticket in TICKETS:
        decision = client.decisions.create(
            model=MODEL,
            input=ticket,
            questions=[
                {
                    "type": "choice",
                    "name": "department",
                    "instructions": "Which department should handle this complaint?",
                    "choices": DEPARTMENTS,
                }
            ],
        )
        answer = require(decision, "department")

        routed = answer.choice
        if answer.confidence < CONFIDENCE_FLOOR:
            routed = f"{answer.choice} -> HUMAN REVIEW (low confidence)"

        print(f"> {ticket}")
        print(f"  routed to: {routed}  (confidence {answer.confidence:.2f})")
        print_distribution(answer)
        print_usage(decision)
        print()


if __name__ == "__main__":
    main()
