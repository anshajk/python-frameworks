"""Shared helpers for the Decisions API demos.

Every demo is runnable on its own; this module only removes the identical
key-loading and answer-unpacking boilerplate.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-6-luna"

# Decisions pricing: input-only, $0.10 per 1M tokens. Output tokens are free.
INPUT_COST_PER_1M = 0.10

# python-frameworks/.env, four levels up from ai/openai/decisions/
REPO_ROOT = Path(__file__).resolve().parents[3]


def get_client() -> OpenAI:
    load_dotenv(REPO_ROOT / ".env")
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError(
            "OPENAI_API_KEY environment variable is not set. "
            f"Add it to {REPO_ROOT / '.env'} or export it in your shell."
        )
    return OpenAI()


def answers_by_name(decision) -> dict:
    return {answer.name: answer for answer in decision.answers}


def require(decision, name):
    """Return the named answer, or raise if the model refused it.

    A refusal is a normal answer type, not an exception, so unpacking code that
    assumes `.probability` or `.choice` will AttributeError without this guard.
    """
    answer = answers_by_name(decision).get(name)
    if answer is None:
        raise KeyError(f"No answer named {name!r} in response")
    if answer.type == "refusal":
        raise RuntimeError(f"Model refused question {name!r}")
    return answer


def decision_cost(decision) -> float:
    return decision.usage.input_tokens / 1_000_000 * INPUT_COST_PER_1M


def print_usage(decision) -> None:
    usage = decision.usage
    print(
        f"  usage: {usage.input_tokens} input / {usage.output_tokens} output tokens"
        f"  (${decision_cost(decision):.8f})"
    )


def print_distribution(answer, indent: str = "  ") -> None:
    for item in answer.probabilities:
        label = getattr(item, "label", None) or item.value
        bar = "#" * round(item.probability * 40)
        print(f"{indent}{str(label):<24} {item.probability:>5.2f} {bar}")
