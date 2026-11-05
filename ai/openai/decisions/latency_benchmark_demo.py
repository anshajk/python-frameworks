"""Decisions vs. Responses + Structured Outputs on the identical task.

Same model (gpt-6-luna), same classification, same input. The difference is
that Decisions constrains the answer space before decoding, while Structured
Outputs generates tokens that happen to validate against a schema.

Cost note: Decisions billing is published ($0.10 / 1M input, output free), so
it is computed here. Generative gpt-6-luna rates are not hardcoded -- pass
--responses-input-cost / --responses-output-cost (per 1M tokens) from the
pricing page if you want that side costed too.

Run:
    python latency_benchmark_demo.py --samples 10
"""

import argparse
import statistics
import time

from _common import INPUT_COST_PER_1M, MODEL, get_client

TICKET = "I was charged twice for my order and nobody has replied to my emails."

CHOICES = [
    {"value": "billing", "description": "Payments, invoices, and refunds."},
    {"value": "technical", "description": "Problems using the product."},
    {"value": "shipping", "description": "Delivery and tracking."},
    {"value": "other", "description": "Requests outside these categories."},
]

SCHEMA = {
    "type": "object",
    "properties": {"department": {"type": "string", "enum": [c["value"] for c in CHOICES]}},
    "required": ["department"],
    "additionalProperties": False,
}

PROMPT = (
    "Which department should handle this complaint? "
    "Options: billing (payments, invoices, refunds), technical (problems using "
    "the product), shipping (delivery and tracking), other (anything else).\n\n"
    f"Complaint: {TICKET}"
)


def time_decisions(client):
    start = time.perf_counter()
    decision = client.decisions.create(
        model=MODEL,
        input=TICKET,
        questions=[
            {
                "type": "choice",
                "name": "department",
                "instructions": "Which department should handle this complaint?",
                "choices": CHOICES,
            }
        ],
    )
    elapsed = (time.perf_counter() - start) * 1000
    return elapsed, decision.usage.input_tokens, decision.usage.output_tokens


def time_responses(client):
    start = time.perf_counter()
    response = client.responses.create(
        model=MODEL,
        input=PROMPT,
        text={"format": {"type": "json_schema", "name": "route", "schema": SCHEMA, "strict": True}},
    )
    elapsed = (time.perf_counter() - start) * 1000
    return elapsed, response.usage.input_tokens, response.usage.output_tokens


def percentile(values, pct):
    ordered = sorted(values)
    index = min(int(len(ordered) * pct / 100), len(ordered) - 1)
    return ordered[index]


def report(label, timings, input_tokens, output_tokens, cost):
    print(f"{label}")
    print(f"  p50 {percentile(timings, 50):7.1f} ms")
    print(f"  p95 {percentile(timings, 95):7.1f} ms")
    print(f"  min {min(timings):7.1f} ms   max {max(timings):7.1f} ms")
    print(f"  mean{statistics.mean(timings):7.1f} ms")
    print(f"  tokens/call: {input_tokens} input, {output_tokens} output")
    print(f"  cost/1k calls: {cost}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=10, help="calls per API (default 10)")
    parser.add_argument("--responses-input-cost", type=float, default=None)
    parser.add_argument("--responses-output-cost", type=float, default=None)
    args = parser.parse_args()

    client = get_client()
    print(f"Model {MODEL}, {args.samples} samples per API, identical routing task\n")

    # One untimed call per API so connection setup is not charged to sample one.
    time_decisions(client)
    time_responses(client)

    dec_times, res_times = [], []
    dec_tokens = res_tokens = None
    for _ in range(args.samples):
        elapsed, tin, tout = time_decisions(client)
        dec_times.append(elapsed)
        dec_tokens = (tin, tout)
    for _ in range(args.samples):
        elapsed, tin, tout = time_responses(client)
        res_times.append(elapsed)
        res_tokens = (tin, tout)

    dec_cost = dec_tokens[0] / 1_000_000 * INPUT_COST_PER_1M * 1000
    report("DECISIONS  /v1/decisions", dec_times, *dec_tokens, f"${dec_cost:.4f}")

    if args.responses_input_cost is not None and args.responses_output_cost is not None:
        res_cost = (
            res_tokens[0] / 1_000_000 * args.responses_input_cost
            + res_tokens[1] / 1_000_000 * args.responses_output_cost
        ) * 1000
        res_cost_label = f"${res_cost:.4f}"
    else:
        res_cost_label = "pass --responses-input-cost/--responses-output-cost to compute"
    report("RESPONSES  /v1/responses + structured outputs", res_times, *res_tokens, res_cost_label)

    speedup = percentile(res_times, 50) / percentile(dec_times, 50)
    print(f"Decisions is {speedup:.1f}x faster at p50 on this task.")
    print(
        f"Decisions generated {dec_tokens[1]} output tokens; "
        f"Responses generated {res_tokens[1]}. You pay for the latter."
    )


if __name__ == "__main__":
    main()
