"""
Root orchestrator for the Trend-to-Content pipeline.

STATUS: STUB. Mimics the shape/timing of the real ADK SequentialAgent
pipeline (README.md section 2) so the SSE endpoint and Streamlit
frontend are demoable before the real agents exist.

IMPORTANT: if app/agents/ already has real trend_scout.py, research.py,
strategy.py, script_writer.py, or qa_editor.py in it from the founder,
do NOT overwrite this file blindly — wire those in here instead of the
_stub_output() calls below.
"""

import asyncio
from typing import AsyncGenerator, Dict, Any

PIPELINE_STEPS = ["trend_scout", "research", "strategy", "script_writer", "qa_editor"]

STEP_LABELS = {
    "trend_scout": "Scouting trending topics",
    "research": "Researching supporting facts",
    "strategy": "Matching to your brand & audience",
    "script_writer": "Writing the script",
    "qa_editor": "QA / final polish",
}


async def run_pipeline(business: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
    state: Dict[str, Any] = {"business": business}

    for step in PIPELINE_STEPS:
        yield {"agent": step, "label": STEP_LABELS[step], "status": "running", "output": None}
        await asyncio.sleep(1.4)
        output = _stub_output(step, state)
        state[step] = output
        yield {"agent": step, "label": STEP_LABELS[step], "status": "done", "output": output}

    yield {"agent": "pipeline", "label": "Complete", "status": "complete", "output": state["qa_editor"]}


def _stub_output(step: str, state: Dict[str, Any]) -> Any:
    biz = state["business"]
    name = biz.get("business_name", "your business")
    biz_type = biz.get("business_type", "business")

    if step == "trend_scout":
        return {"topics": [
            {"title": "Behind-the-scenes daily process", "why": f"Rising this week for {biz_type} accounts."},
            {"title": "Customer FAQ answered on camera", "why": "Builds trust faster than promo content."},
        ]}
    if step == "research":
        return {"notes": "Supporting stats and angles for the chosen topic (stub)."}
    if step == "strategy":
        return {"angle": f"Framed for {biz.get('target_audience', 'your audience')} on {biz.get('platform', 'Instagram')}."}
    if step == "script_writer":
        return {
            "hook": f'"This is what a real day looks like at {name}."',
            "shot_list": [
                "Open on the hook, spoken to camera.",
                "Show the real process, handheld and unpolished.",
                "Cut to the result or reaction.",
                "End with a simple line for the audience.",
            ],
            "caption": f"A real look inside {name}. 🌱",
            "hashtags": ["#smallbusiness", f"#{biz_type.replace(' ', '')}"],
        }
    if step == "qa_editor":
        prev = state.get("script_writer", {})
        return {**prev, "qa_notes": "Tone check passed. Within platform character limits."}
    return {}
