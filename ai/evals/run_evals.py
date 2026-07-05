"""Programmatic eval run — a stand-in for a CI regression gate.

Unlike the pytest entry point, this runs the whole golden set through DeepEval's
``evaluate()`` and prints a scorecard. In a real pipeline you'd inspect the returned
results and fail the build if the aggregate pass rate drops below a threshold.

    export OPENAI_API_KEY=...
    python ai/evals/run_evals.py
"""

from deepeval import evaluate

from golden_dataset import GOLDEN_DATASET
from metrics import answer_relevancy, faithfulness, task_success, tool_correctness
from test_agent_evals import build_test_case

# Faithfulness needs retrieval context, so we can't blindly apply it to every case. We
# split the golden set into "grounded" runs (KB was searched) and the rest, and evaluate
# each group with the metrics that actually apply.
BASE_METRICS = [task_success, tool_correctness, answer_relevancy]


def main() -> None:
    test_cases = [build_test_case(case) for case in GOLDEN_DATASET]
    grounded = [tc for tc in test_cases if tc.retrieval_context]
    ungrounded = [tc for tc in test_cases if not tc.retrieval_context]

    if grounded:
        evaluate(test_cases=grounded, metrics=BASE_METRICS + [faithfulness])
    if ungrounded:
        evaluate(test_cases=ungrounded, metrics=BASE_METRICS)


if __name__ == "__main__":
    main()
