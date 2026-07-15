# Multi-agent patterns with ADK and Microsoft Agent Framework

Companion code for the *"Multi-Agent Systems"* article. Fresh, focused examples that each
demonstrate one architecture pattern in one of the two frameworks.

## What's here

| File | Framework | Pattern |
| --- | --- | --- |
| `adk/research_team/` | Google ADK | Concurrent fan-out (`ParallelAgent`) + sequential fan-in (`SequentialAgent`), shared session state via `output_key` |
| `adk/writer_critic_loop/` | Google ADK | Reflection loop (`LoopAgent`) with `max_iterations` cap + `exit_loop` escalation |
| `adk/support_coordinator/` | Google ADK | LLM-driven delegation (coordinator `LlmAgent` + `sub_agents`, `transfer_to_agent`) |
| `agent_framework/concurrent_analysts.py` | Microsoft Agent Framework | Concurrent orchestration (`ConcurrentBuilder`) with a custom aggregator |
| `agent_framework/triage_handoff.py` | Microsoft Agent Framework | Handoff / dynamic routing (`HandoffBuilder`) |

## Setup

```bash
pip install google-adk agent-framework

# Google ADK (Gemini via AI Studio key, or configure Vertex AI)
export GOOGLE_API_KEY=...

# Microsoft Agent Framework examples use OpenAI
export OPENAI_API_KEY=...
```

## Run

**ADK** examples are agent packages — run them with the `adk` CLI:

```bash
adk run ai/multi_agent/adk/research_team
adk run ai/multi_agent/adk/writer_critic_loop
adk run ai/multi_agent/adk/support_coordinator
# or open the dev UI for any of them:
adk web ai/multi_agent/adk
```

**Microsoft Agent Framework** examples are standalone scripts:

```bash
python ai/multi_agent/agent_framework/concurrent_analysts.py
python ai/multi_agent/agent_framework/triage_handoff.py
```

> `google-adk` and `agent-framework` are installed ad hoc (not pinned in the repo
> `requirements.txt`), consistent with how experiments here manage dependencies. Model IDs
> (`gemini-2.0-flash`, `gpt-4o-mini`) can be swapped at the top of each file.
