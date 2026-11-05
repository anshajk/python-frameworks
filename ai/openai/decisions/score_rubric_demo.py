"""Score questions: rate an input against ordered levels.

The returned `score` is a probability-weighted average of the level *indices*
(0-based), so it can land between levels. That makes it a summary of a
distribution, not a label.

A score of 1.0 can mean "confidently level 1" or "torn between 0 and 2".
This demo recomputes the score by hand to show where the number comes from,
and prints the distribution so you can tell those two cases apart.

Run:
    python score_rubric_demo.py
"""

from _common import MODEL, get_client, print_distribution, print_usage, require

LEVELS = [
    {"label": "Cosmetic", "description": "Appearance only; no lost functionality."},
    {"label": "Workaround available", "description": "A task fails, but another way works."},
    {"label": "Fully blocked", "description": "A task fails with no workaround."},
]

ISSUES = [
    "Export fails in Safari but works in Chrome.",
    "The sign-up button is 2px off-centre on mobile.",
    "Login is down for all users, nobody can get in.",
    "Sometimes the dashboard loads, sometimes it 500s. Hard to say.",
]


def main() -> None:
    client = get_client()
    print("Scoring issues against a 3-level severity rubric")
    print("levels: " + ", ".join(f"{i}={lvl['label']}" for i, lvl in enumerate(LEVELS)) + "\n")

    for issue in ISSUES:
        decision = client.decisions.create(
            model=MODEL,
            input=issue,
            questions=[
                {
                    "type": "score",
                    "name": "severity",
                    "instructions": "How severe is this issue?",
                    "levels": LEVELS,
                }
            ],
        )
        answer = require(decision, "severity")

        recomputed = sum(item.value * item.probability for item in answer.probabilities)
        top = max(answer.probabilities, key=lambda item: item.probability)

        print(f"> {issue}")
        print(f"  score {answer.score:.2f}  (confidence {answer.confidence:.2f})")
        print(f"  weighted average of indices = {recomputed:.2f}")
        print(f"  most likely level: {top.label} at p={top.probability:.2f}")
        if answer.confidence < 0.60:
            print("  !! low confidence -- the score is averaging disagreement, not grading")
        print_distribution(answer)
        print_usage(decision)
        print()


if __name__ == "__main__":
    main()
