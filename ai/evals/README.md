# Evaluating an agent with DeepEval

Companion code for the *"Evaluating Agentic Systems"* article. A tiny support-triage
agent (`agent.py`) is evaluated end to end with [DeepEval](https://deepeval.com).

## Files

| File | Role |
| --- | --- |
| `agent.py` | The agent under test. Two tools; returns answer **and** trajectory + retrieval context. |
| `golden_dataset.py` | Hand-curated golden cases: input, expected tools, reference answer. |
| `metrics.py` | The metric basket: task success (G-Eval), tool correctness, faithfulness, answer relevancy. |
| `test_agent_evals.py` | Pytest-style evals via `deepeval test run`. |
| `run_evals.py` | Programmatic `evaluate()` scorecard — a CI-gate stand-in. |

## Setup

```bash
pip install deepeval openai
export OPENAI_API_KEY=...   # used by BOTH the agent and the DeepEval judge
```

## Run

```bash
# See one trajectory (answer + tools called)
python ai/evals/agent.py

# Full eval suite (pytest-style)
deepeval test run ai/evals/test_agent_evals.py

# A single case
deepeval test run ai/evals/test_agent_evals.py -k "refund"

# Programmatic scorecard
python ai/evals/run_evals.py
```

> DeepEval is not in the repo's `requirements.txt`; install it ad hoc as above (consistent
> with how experiments in this repo manage dependencies). The judge model defaults to
> OpenAI — swap it in `metrics.py` if you prefer a different judge.
