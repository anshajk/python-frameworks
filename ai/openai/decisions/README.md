# OpenAI Decisions API

Companion code for the compute post on the Decisions API (public beta, October 2026).

The Decisions API answers **bounded** questions. Instead of generating text that you then
parse and validate, you declare the answer space up front and get back a typed answer with
calibrated probabilities. `POST /v1/decisions`, `gpt-6-luna` only.

| Question type | Returns | Use for |
| --- | --- | --- |
| `predicate` | `probability` (0–1) | yes/no gates, relevance, policy checks |
| `choice` | `choice`, `probabilities[]`, `confidence` | routing, categorisation |
| `score` | `score`, `probabilities[]`, `confidence` | severity, rubrics, prioritisation |

## Setup

Requires the OpenAI Python SDK **≥ 3.26.0** — `client.decisions` does not exist on v2.x.
Because that is a major-version jump from what the sibling `ai/openai/` demos use, this
folder keeps its own virtualenv rather than upgrading the shared install.

There are only two dependencies. `image_predicate_demo.py` makes plain HTTP calls with
`httpx2`, which already ships with the OpenAI SDK — note the `2` suffix, as SDK v3 moved off
`httpx`.

```bash
cd ai/openai/decisions
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Set `OPENAI_API_KEY` in `python-frameworks/.env` (git-ignored) or export it in your shell.
Every script loads it via `_common.get_client()` and raises a clear error if it is missing.

## The demos

Each script is standalone — run it directly.

```bash
.venv/bin/python choice_router_demo.py
```

| Script | What it shows |
| --- | --- |
| `predicate_demo.py` | Calibrated yes/no probabilities for passage relevance. |
| `image_predicate_demo.py` | Image predicates scored against real labelled photographs, with a precision/recall sweep. |
| `choice_router_demo.py` | Ticket routing with an `other` fallback; prints the full distribution, not just the winner. |
| `score_rubric_demo.py` | Severity scoring, recomputing the score by hand to show it is a weighted average of level indices. |
| `multi_question_demo.py` | Batching independent questions into one request, and why dependent questions need two. |
| `latency_benchmark_demo.py` | Decisions vs. Responses + Structured Outputs on the identical task, same model. |
| `threshold_tuning_demo.py` | Sweeps thresholds over a labelled set to show the precision/recall tradeoff. |
| `agent_gate_demo.py` | Decisions as a pre-flight gate (scope, injection, tool choice, complexity) before any generative call. |

`_common.py` holds shared key-loading and answer-unpacking helpers.

## What the demos actually showed

Measured on this account, October 2026. Your numbers will vary.

**Decisions was ~16x faster than the Responses API** on the same routing task with the same
model — p50 135 ms vs. 2209 ms. The documented claim is ~10x, so that held up comfortably.

**Output tokens really are zero.** Every response reports `usage.output_tokens == 0`, which
is why billing is input-only at $0.10/1M. A routing call costs about **$0.000016**, or
roughly **$0.015 per 1000 calls**.

**`confidence` is not the top probability.** One ambiguous ticket returned `billing` at
probability 0.80 but `confidence` 0.73. They are separate signals — threshold on the one
that matches your question.

**The 0.5 default is usually wrong.** In `threshold_tuning_demo.py` the optimal boundary is
**0.35**; at 0.5 the model misses a genuinely urgent ticket that scored 0.44. There is no
universal threshold — derive it from labelled examples and the relative cost of a false
positive versus a false negative.

**It ignores theatrical wording.** "Our staging environment is completely down" scored 0.00
for urgency and "URGENT!!! Please add dark mode" scored 0.05, while a calmly-worded failing
billing job scored 0.86. The instructions did say to judge impact over insistence.

**Vision holds up on real photographs.** On 30 labelled concrete images (15 cracked, 15
intact) the predicate scored **30/30 across every threshold from 0.15 to 0.85**, including
the naive 0.5 default. The distribution is sharply bimodal — intact surfaces cluster at
0.03–0.11, cracked ones at 0.87–0.99 — so there is a wide band of thresholds that all work.
Total cost for the run: **$0.000765**.

Two caveats on that result. This is an easy, high-contrast task, and a 30-image sample is
far too small to publish an accuracy figure from. An earlier run that sampled different
images produced one false positive, an intact surface scoring 0.69. Treat the bimodality as
the finding, not the perfect score: when a predicate separates this cleanly, the exact
threshold barely matters, and the few inputs that land in the middle are precisely the ones
worth routing to a human.

## Gotchas

- **Images must be inline base64 data URLs.** Hosted `http(s)` URLs and `file_id` inputs are
  rejected by this endpoint, unlike the Responses API.
- **`refusal` is an answer type, not an exception.** Any answer can come back as
  `{"type": "refusal"}`, so code that reaches straight for `.probability` or `.choice` will
  `AttributeError`. `_common.require()` guards this.
- **Score levels are 0-indexed**, and `score` is a probability-weighted average of those
  indices — so it can land *between* levels. A score of 1.0 may mean "confidently level 1"
  or "split between 0 and 2". Check `confidence` and the distribution to tell them apart.
- **Batched questions cannot branch.** Questions in one request are evaluated against the
  same input independently. If B depends on A's answer, send two requests.
- **Always include a fallback choice.** Without an `other` option the model must assign
  every input to a category, including ones your taxonomy does not cover.
- **Type-safe is not the same as correct.** The schema guarantees you get a valid option; it
  does not guarantee the right one. This moves failures from crashes you notice to wrong
  answers you do not.

## Dataset

`image_predicate_demo.py` samples from
[`mohammadnajeeb/concrete_crack_images`](https://huggingface.co/datasets/mohammadnajeeb/concrete_crack_images),
licensed **CC-BY-4.0** — 227×227 photographs of concrete surfaces labelled `Negative` (no
crack) and `Positive` (crack).

The dataset is never bulk-downloaded. The Hugging Face datasets-server exposes per-row image
URLs, so only the sampled images are fetched. A default 30-image run transfers a few hundred
KB and costs under a cent in API calls; the estimate is printed before any request is made.
Use `--limit` to change the sample size and `--seed` to vary which images are drawn.

## When not to use it

Reach for **Structured Outputs** when you need extracted fields or written explanations, and
**function calling** when the model should request a tool with arguments. Decisions only
fits when every valid outcome is enumerable in advance.

## Prior art

TypeSafe AI's **Jev** shipped the same three primitives (`noul`/`choice`/`score`) on
15 September 2026, three weeks before this beta, billing input-only at $0.042/1M. Two teams
converging on the same shape within a month suggests this is a real missing layer rather
than a product gimmick. Jev is waitlist-gated, so there is no runnable Jev code here.
