# project-Y
building creator agent for biz owners
# Trend-to-Content Multi-Agent System — Project Plan

Stack: **Python + FastAPI + Google ADK + Gemini Flash**
Scope: single business now, designed to extend to multi-tenant later.

---

## 1. Why this stack

- **Google ADK** — open-source, purpose-built for multi-agent orchestration (sequential, parallel, and LLM-routed agent hierarchies). Free to use; you only pay for model calls.
- **Gemini 2.5 Flash / Flash-Lite** — cheapest capable models on the market right now, with a free tier through Google AI Studio (good enough for dev + early production). ADK also supports LiteLLM, so you can swap in Claude, GPT, or open models later without rewriting agent logic.
- **FastAPI** — thin API layer in front of the agent pipeline, easy to containerize and scale later.
- Free/cheap data sources to start: `pytrends` (Google Trends, free), Reddit API (free tier), RSS/news feeds (free), YouTube Data API (free quota). Avoid paid X/Twitter API until you need it.

---

## 2. Agent architecture

One **root/orchestrator agent** runs a `SequentialAgent` pipeline of 5 sub-agents. Each sub-agent's output becomes the next agent's input via ADK's shared session state.

1. **Trend Scout Agent** — tools: Google Trends, Reddit, RSS/news APIs. Outputs a shortlist of trending topics relevant to the business's industry/niche.
2. **Research Agent** — takes a chosen trend, pulls supporting facts, stats, and angles (web search tool).
3. **Strategy Agent** — maps the trend + research to the business's brand voice, goals, and target audience (pulled from a stored business profile).
4. **Script Writer Agent** — generates the actual content: reel/short script, caption, blog draft, etc., in the requested format.
5. **QA/Editor Agent** — checks tone consistency, factual claims, banned words/compliance, and platform constraints (character limits, hashtags).

Later, you can add: a **Scheduler Agent** (posts or queues content) and a **Analytics/Feedback Agent** (feeds performance data back to Strategy).

---

## 3. Repository structure

```
content-agent-platform/
├── README.md
├── .env.example
├── .gitignore
├── pyproject.toml              # or requirements.txt
├── docker-compose.yml          # api + postgres + redis for local dev
├── Dockerfile
│
├── app/
│   ├── main.py                 # FastAPI entrypoint
│   ├── config.py                # settings, env vars, model config
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py     # root SequentialAgent wiring all sub-agents
│   │   ├── trend_scout.py
│   │   ├── research.py
│   │   ├── strategy.py
│   │   ├── script_writer.py
│   │   └── qa_editor.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── google_trends.py    # pytrends wrapper
│   │   ├── reddit.py
│   │   ├── news_rss.py
│   │   └── web_search.py
│   │
│   ├── models/
│   │   ├── business_profile.py # brand voice, audience, tone, banned words
│   │   ├── content_request.py
│   │   └── content_output.py
│   │
│   ├── api/
│   │   ├── routes_content.py   # POST /generate, GET /content/{id}
│   │   └── routes_business.py  # CRUD for business profile
│   │
│   ├── db/
│   │   ├── session.py
│   │   └── repository.py
│   │
│   └── prompts/
│       ├── trend_scout.txt
│       ├── research.txt
│       ├── strategy.txt
│       ├── script_writer.txt
│       └── qa_editor.txt
│
├── tests/
│   ├── test_agents.py
│   └── test_api.py
│
├── evals/                      # ADK's built-in agent evaluation suite
│   └── content_pipeline.evalset.json
│
└── scripts/
    └── seed_business_profile.py
```

Keep prompts as separate `.txt`/`.jinja` files, not hardcoded strings — makes iterating on agent behavior much faster and is standard ADK practice.

---

## 4. Step-by-step build plan

### Phase 0 — Setup (day 1)
- Create the repo, virtualenv, install `google-adk`, `fastapi`, `uvicorn`, `pytrends`, `praw` (Reddit).
- Get a free Gemini API key from Google AI Studio. Set `GOOGLE_API_KEY` in `.env`.
- Confirm you can run ADK's local dev UI (`adk web`) with a single "hello world" agent — this is the fastest way to test agents in isolation before wiring the API.

### Phase 1 — Single agent, single tool (days 2–3)
- Build the **Trend Scout Agent** alone. Give it one tool (`pytrends`). Test it in `adk web` with a hardcoded niche like "coffee shops."
- Get comfortable with ADK's agent/tool/session model before adding complexity.

### Phase 2 — Business profile (day 4)
- Define the `BusinessProfile` model: brand voice, tone words, audience, platforms used, banned topics/words.
- Store it in SQLite/Postgres. Write a `seed_business_profile.py` script so you can test with your own business data immediately.

### Phase 3 — Build out remaining agents (days 5–8)
- Add Research, Strategy, Script Writer, QA agents one at a time, each testable standalone in `adk web` before chaining.
- Write clear, narrow prompts for each — each agent should do one job well rather than one agent trying to do everything.

### Phase 4 — Chain into orchestrator (days 9–10)
- Wire all 5 into a `SequentialAgent` (or `LlmAgent` with sub_agents for dynamic routing if you want the orchestrator to skip/reorder steps).
- Test the full pipeline end-to-end via `adk web` with a real business profile.

### Phase 5 — Wrap in FastAPI (days 11–12)
- `POST /generate` — takes business_id + content type (reel/blog/post) → runs pipeline → returns script.
- `GET /content/{id}` — retrieve past generated content.
- Add basic auth (API key header) even for a single-business MVP — you'll thank yourself later.

### Phase 6 — Cost & quality controls (days 13–14)
- Set `max_output_tokens` and use Flash-Lite for the Trend Scout/Research steps (cheap, high-volume), reserve Flash (or Pro) only for Script Writer if quality needs a bump.
- Add ADK eval sets so you can catch regressions when you tweak prompts.
- Add simple caching (Redis or in-memory) for trend data — no need to refetch Google Trends every request.

### Phase 7 — Ship a thin frontend (days 15+)
- Simple form (business owner picks content type + platform) → calls your API → shows the generated script with edit/approve buttons.
- Can be a basic React app, or even a Streamlit app for the MVP.

### Phase 8 — Prep for multi-tenant (later)
- Move `business_id` scoping into every table/query now, even with one business, so expanding to multiple businesses later is a config change, not a rewrite.
- Add per-business rate limiting and API key management when you onboard a second user.

---

## 5. Cost-saving notes

- Gemini Flash-Lite is cheapest for high-frequency, low-complexity agents (trend scouting, research summarizing).
- Cache trend/news data — most business niches don't need trend refreshes more than a few times a day.
- Batch: if generating content for multiple platforms, do it in one agent call with structured JSON output rather than 3 separate calls.
- Use ADK's built-in tracing/eval tools to catch prompt bloat (unnecessarily long system prompts cost money on every call).
