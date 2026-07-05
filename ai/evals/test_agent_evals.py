"""Pytest-style evals for the support-triage agent.

Run the whole suite:

    export OPENAI_API_KEY=...
    deepeval test run ai/evals/test_agent_evals.py

Run a single case (the journey that needs both tools):

    deepeval test run ai/evals/test_agent_evals.py -k "refund"
"""

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase, ToolCall

from agent import run_agent
from golden_dataset import GOLDEN_DATASET
from metrics import answer_relevancy, faithfulness, task_success, tool_correctness


def build_test_case(case) -> LLMTestCase:
    """Run the agent for one golden case and wrap it as an LLMTestCase."""
    result = run_agent(case["input"])
    return LLMTestCase(
        input=case["input"],
        actual_output=result.answer,
        expected_output=case["reference_answer"],
        retrieval_context=result.retrieval_context or None,
        tools_called=[ToolCall(name=step["tool"]) for step in result.trajectory],
        expected_tools=[ToolCall(name=name) for name in case["expected_tools"]],
    )


def metrics_for(test_case: LLMTestCase):
    """Faithfulness only applies when there is retrieved context to be faithful to."""
    metrics = [task_success, tool_correctness, answer_relevancy]
    if test_case.retrieval_context:
        metrics.append(faithfulness)
    return metrics


@pytest.mark.parametrize(
    "case", GOLDEN_DATASET, ids=[c["input"][:24] for c in GOLDEN_DATASET]
)
def test_agent(case):
    test_case = build_test_case(case)
    assert_test(test_case, metrics_for(test_case))
