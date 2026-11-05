"""Turning calibrated probabilities into a decision boundary.

The API gives you a probability. It cannot give you a threshold, because a
threshold encodes how much a false positive costs relative to a false negative
-- and that is a product question, not a model question.

This demo scores a small labelled set once, then sweeps every threshold to show
how precision and recall trade off. It picks two boundaries: the best F1, and
the best expected cost when a miss hurts more than a false alarm.

Run:
    python threshold_tuning_demo.py --fn-cost 5
"""

import argparse

from _common import MODEL, get_client, require

QUESTION = (
    "Does this message describe a problem that is blocking real customers from "
    "working right now, or that will cause harm within the next 24 hours if "
    "nobody acts? Judge the actual impact, not how insistent the wording is. "
    "Problems in non-production environments are not urgent."
)

# Deliberately hard: several urgent cases are worded calmly, and several routine
# ones are worded like emergencies. A separable dataset would make every
# threshold look equally good and teach you nothing.
# (message, is_urgent)
LABELLED = [
    ("Production is down, no users can log in at all.", True),
    ("Payments are failing for every checkout since the deploy.", True),
    ("Our nightly billing job has failed three times; invoices go out at 6am.", True),
    ("Only one customer affected, but it is our largest account and they are fully blocked.", True),
    ("Checkout works but confirmation emails never arrive, so people are ordering twice.", True),
    ("Noticed the SSL certificate expires tomorrow morning.", True),
    ("I cannot access my account and I have a client demo in an hour.", True),
    ("Two of our twelve integrations have been erroring since lunch.", True),
    ("URGENT!!! Please add dark mode, this is really important to us.", False),
    ("Our staging environment is completely down.", False),
    ("Critical: there is a typo in the pricing page heading.", False),
    ("Everything is broken on my old browser from 2016.", False),
    ("This is the third time I have asked about the roadmap!", False),
    ("A scheduled report arrived about 20 minutes late this morning.", False),
    ("Login is slow sometimes, maybe 3 seconds, not a huge deal.", False),
    ("We hit a rate limit yesterday but it cleared up on its own.", False),
    ("Just wanted to say the new release is great.", False),
    ("How do I change my billing address?", False),
]


def score_dataset(client):
    print(f"Scoring {len(LABELLED)} labelled messages...\n")
    scored = []
    for message, is_urgent in LABELLED:
        decision = client.decisions.create(
            model=MODEL,
            input=message,
            questions=[{"type": "predicate", "name": "is_urgent", "instructions": QUESTION}],
        )
        probability = require(decision, "is_urgent").probability
        scored.append((message, is_urgent, probability))
        mark = "URGENT" if is_urgent else "routine"
        print(f"  p={probability:.2f}  gold={mark:<8} {message[:58]}")
    return scored


def evaluate(scored, threshold):
    tp = sum(1 for _, gold, p in scored if gold and p >= threshold)
    fp = sum(1 for _, gold, p in scored if not gold and p >= threshold)
    fn = sum(1 for _, gold, p in scored if gold and p < threshold)
    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1, fp, fn


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fn-cost", type=float, default=5.0, help="cost of a miss (default 5)")
    parser.add_argument("--fp-cost", type=float, default=1.0, help="cost of a false alarm")
    args = parser.parse_args()

    client = get_client()
    scored = score_dataset(client)

    thresholds = [i / 20 for i in range(1, 20)]
    print(f"\n{'thresh':>7} {'prec':>6} {'recall':>7} {'F1':>6} {'FP':>4} {'FN':>4} {'cost':>7}")
    print("-" * 46)

    rows = []
    for threshold in thresholds:
        precision, recall, f1, fp, fn = evaluate(scored, threshold)
        cost = fp * args.fp_cost + fn * args.fn_cost
        rows.append((threshold, precision, recall, f1, fp, fn, cost))
        print(
            f"{threshold:>7.2f} {precision:>6.2f} {recall:>7.2f} {f1:>6.2f} "
            f"{fp:>4} {fn:>4} {cost:>7.1f}"
        )

    best_f1 = max(rows, key=lambda r: r[3])
    best_cost = min(rows, key=lambda r: r[6])

    print(f"\nBest F1      : threshold {best_f1[0]:.2f}  (F1 {best_f1[3]:.2f})")
    print(
        f"Lowest cost  : threshold {best_cost[0]:.2f}  "
        f"(cost {best_cost[6]:.1f} at FN={args.fn_cost}x, FP={args.fp_cost}x)"
    )
    if best_f1[0] != best_cost[0]:
        print(
            "\nThese disagree. When a miss costs more than a false alarm, the right "
            "boundary sits lower than the one that maximises F1."
        )


if __name__ == "__main__":
    main()
