"""ADK multi-agent example: concurrent fan-out + sequential fan-in.

Demonstrates two patterns composed together for the "Multi-Agent Systems" article:

* a ``ParallelAgent`` fans work out to three specialist researchers that run
  concurrently, each writing its findings to a distinct key in shared session state;
* a ``SequentialAgent`` then runs a synthesizer that reads those three state keys
  (fan-in) and produces one combined brief.

Communication here is via **shared session state** (`output_key`), which is ADK's
substrate for passing data between agents.

Run it:

    export GOOGLE_API_KEY=...   # or configure Vertex AI
    adk run ai/multi_agent/adk/research_team
"""

from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent

GEMINI_MODEL = "gemini-2.0-flash"

market_researcher = LlmAgent(
    name="MarketResearcher",
    model=GEMINI_MODEL,
    description="Researches market size, demand, and competition for a topic.",
    instruction=(
        "You are a market analyst. For the user's topic, summarise market size, "
        "demand trends, and the competitive landscape in 3-4 concise bullet points."
    ),
    output_key="market_findings",
)

tech_researcher = LlmAgent(
    name="TechResearcher",
    model=GEMINI_MODEL,
    description="Researches the technical landscape and maturity for a topic.",
    instruction=(
        "You are a technology analyst. For the user's topic, summarise the key "
        "technologies, their maturity, and technical risks in 3-4 concise bullet points."
    ),
    output_key="tech_findings",
)

risk_researcher = LlmAgent(
    name="RiskResearcher",
    model=GEMINI_MODEL,
    description="Researches regulatory, financial, and operational risks for a topic.",
    instruction=(
        "You are a risk analyst. For the user's topic, summarise the main regulatory, "
        "financial, and operational risks in 3-4 concise bullet points."
    ),
    output_key="risk_findings",
)

# Fan-out: the three researchers run concurrently, not one after another.
parallel_research = ParallelAgent(
    name="ParallelResearch",
    sub_agents=[market_researcher, tech_researcher, risk_researcher],
    description="Runs the three specialist researchers in parallel.",
)

# Fan-in: read the three state keys the researchers wrote and synthesise them.
synthesizer = LlmAgent(
    name="Synthesizer",
    model=GEMINI_MODEL,
    description="Combines the specialist findings into a single brief.",
    instruction=(
        "You are a lead analyst. Combine the findings below into one coherent "
        "executive brief with a short recommendation.\n\n"
        "Market findings:\n{market_findings}\n\n"
        "Technology findings:\n{tech_findings}\n\n"
        "Risk findings:\n{risk_findings}"
    ),
    output_key="final_brief",
)

# The pipeline: fan-out (parallel) THEN fan-in (synthesizer), in order.
root_agent = SequentialAgent(
    name="ResearchTeam",
    sub_agents=[parallel_research, synthesizer],
    description="Concurrent research fan-out followed by a synthesis step.",
)
