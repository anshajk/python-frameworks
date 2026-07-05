"""DeepEval metrics for the support-triage agent.

Each metric here maps directly to a row in the "metrics that matter" table from the
article. Together they describe what "good" means for this agent: it must succeed at the
task, call the right tools (the journey), stay grounded in tool output, and stay on topic.

The judge model defaults to OpenAI, so ``OPENAI_API_KEY`` must be set.
"""

from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    GEval,
    ToolCorrectnessMetric,
)
from deepeval.test_case import LLMTestCaseParams

# Destination: did the agent actually accomplish the user's goal? LLM-as-judge via G-Eval.
task_success = GEval(
    name="Task Success",
    criteria=(
        "Determine whether the actual output accomplishes the user's request and is "
        "consistent with the expected output. Penalise answers that are confidently "
        "wrong or that fail to address the question."
    ),
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.EXPECTED_OUTPUT,
    ],
    threshold=0.7,
)

# Journey: were the right tools chosen? (name-level matching, order-insensitive)
tool_correctness = ToolCorrectnessMetric(threshold=0.9)

# Safety: is the answer grounded in the retrieved knowledge-base context?
faithfulness = FaithfulnessMetric(threshold=0.8)

# Capability: does the answer actually address the question that was asked?
answer_relevancy = AnswerRelevancyMetric(threshold=0.7)


def all_metrics():
    """Return the full metric basket used for end-to-end evaluation."""
    return [task_success, tool_correctness, faithfulness, answer_relevancy]
