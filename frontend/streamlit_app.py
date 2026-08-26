import json
import os

import requests
import streamlit as st
import streamlit.components.v1 as components

API_BASE = os.environ.get("API_BASE", "http://localhost:8000")

st.set_page_config(page_title="Project Y", page_icon="🌱", layout="centered")

# ---------------------------------------------------------------- dark ChatGPT-style theme
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        color: #ECECEC;
    }
    .stApp { background-color: #212121; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 4rem; max-width: 720px; position: relative; z-index: 1; }

    h1, h2, h3 { color: #ECECEC; font-weight: 600; letter-spacing: -0.01em; }

    .py-logo { display:flex; align-items:center; gap:9px; justify-content:center; margin-bottom: 8px; }
    .py-logo .mark { font-size: 22px; }
    .py-logo .word { font-size: 19px; font-weight: 600; color:#ECECEC; }
    .py-tag { text-align:center; color: #9B9B9B; font-size: 14.5px; margin-bottom: 44px; }

    div[data-testid="stTextArea"] textarea {
        background: #2F2F2F !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 18px !important;
        padding: 18px 20px !important;
        font-size: 15.5px !important;
        color: #ECECEC !important;
        box-shadow: 0 8px 30px rgba(0,0,0,0.35) !important;
        min-height: 96px !important;
    }
    div[data-testid="stTextArea"] textarea::placeholder { color: #8E8E8E !important; }
    div[data-testid="stTextArea"] textarea:focus {
        border-color: #10A37F !important;
        box-shadow: 0 0 0 1px #10A37F !important;
    }
    div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background: #2F2F2F !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: #ECECEC !important;
    }
    div[data-testid="stTextInput"] input::placeholder { color: #8E8E8E !important; }

    .stButton button {
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        background: #10A37F !important;
        color: #fff !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 9px 18px !important;
    }
    .stButton button:hover { background: #15B98B !important; }

    div[role="radiogroup"] label { color: #ECECEC !important; }
    div[role="radiogroup"] label div:first-child { border-color: rgba(255,255,255,0.3) !important; }

    .py-chip-label { font-size: 12.5px; color: #8E8E8E; margin: 20px 0 6px; text-transform: uppercase; letter-spacing: 0.04em; }

    .py-thread { margin-top: 90px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 40px; }
    .py-thread-title { font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; color: #6E6E6E; margin-bottom: 28px; }
    .py-step-row { display:flex; gap:16px; position:relative; padding-bottom: 30px; }
    .py-step-row:not(:last-child)::before {
        content:''; position:absolute; left:11px; top:26px; bottom:0; width:1px; background: rgba(255,255,255,0.1);
    }
    .py-step-num {
        flex-shrink:0; width:24px; height:24px; border-radius:50%; background:#2F2F2F;
        border:1px solid rgba(255,255,255,0.15); display:flex; align-items:center; justify-content:center;
        font-size:11.5px; font-weight:600; color: #9B9B9B; z-index:1;
    }
    .py-step-body h4 { font-size: 15px; font-weight:600; margin-bottom:3px; color:#ECECEC; }
    .py-step-body p { font-size: 13.5px; color: #9B9B9B; line-height:1.5; margin:0; }

    .py-status-row { display:flex; align-items:center; gap:10px; padding:9px 0; font-size:14.5px; }
    .py-status-dot { width:8px; height:8px; border-radius:50%; background: rgba(255,255,255,0.15); flex-shrink:0; }
    .py-status-dot.running { background: #10A37F; box-shadow: 0 0 8px rgba(16,163,127,0.6); }
    .py-status-dot.done { background: #ECECEC; }
    .py-status-row.pending span { color: #6E6E6E; }
    .py-status-row.done span { color: #ECECEC; }

    .py-result { border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 22px 24px; margin-top: 20px; background: #2A2A2A; }
    .py-result .label { font-size:11.5px; text-transform:uppercase; letter-spacing:.04em; color:#10A37F; margin: 14px 0 4px; }
    .py-result .label:first-child { margin-top:0; }
    .py-result p, .py-result li { color: #DDDDDD; }
    .py-tag-pill { display:inline-block; background:#2F2F2F; border:1px solid rgba(255,255,255,0.1); border-radius:6px; padding:2px 8px; font-size:12.5px; margin-right:6px; color:#ECECEC; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- cursor-follow glow (background effect)
components.html(
    """
    <script>
    (function() {
        const doc = window.parent.document;
        if (doc.getElementById('py-cursor-glow')) return;

        const glow = doc.createElement('div');
        glow.id = 'py-cursor-glow';
        Object.assign(glow.style, {
            position: 'fixed', top: '0', left: '0',
            width: '620px', height: '620px', borderRadius: '50%',
            pointerEvents: 'none', zIndex: '0',
            background: 'radial-gradient(circle, rgba(16,163,127,0.10) 0%, rgba(16,163,127,0) 70%)',
            transform: 'translate(-50%, -50%)',
            transition: 'left 0.06s linear, top 0.06s linear',
        });
        doc.body.appendChild(glow);

        doc.addEventListener('mousemove', (e) => {
            glow.style.left = e.clientX + 'px';
            glow.style.top = e.clientY + 'px';
        });
    })();
    </script>
    """,
    height=0,
)

# ---------------------------------------------------------------- state
if "stage" not in st.session_state:
    st.session_state.stage = "landing"      # landing -> details -> results
if "description" not in st.session_state:
    st.session_state.description = ""
if "biz" not in st.session_state:
    st.session_state.biz = {}

STEP_ORDER = ["trend_scout", "research", "strategy", "script_writer", "qa_editor"]
STEP_LABELS = {
    "trend_scout": "Scouting trending topics",
    "research": "Researching supporting facts",
    "strategy": "Matching to your brand & audience",
    "script_writer": "Writing the script",
    "qa_editor": "QA / final polish",
}

# ---------------------------------------------------------------- header
st.markdown(
    '<div class="py-logo"><span class="mark">🌱</span><span class="word">Project Y</span></div>'
    '<div class="py-tag">Turn what\'s trending into a content idea made for your business.</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- LANDING
if st.session_state.stage == "landing":
    desc = st.text_area(
        "desc", placeholder="Tell us about your business — what you sell, and who it's for…",
        label_visibility="collapsed", height=100,
    )
    c1, c2 = st.columns([5, 1])
    with c2:
        if st.button("Start →", use_container_width=True):
            if desc.strip():
                st.session_state.description = desc.strip()
                st.session_state.stage = "details"
                st.rerun()

# ---------------------------------------------------------------- DETAILS
elif st.session_state.stage == "details":
    st.markdown(f"**Your business:** {st.session_state.description}")
    if st.button("← Edit"):
        st.session_state.stage = "landing"
        st.rerun()

    st.markdown('<div class="py-chip-label">Business name</div>', unsafe_allow_html=True)
    biz_name = st.text_input("bn", placeholder="e.g. Amara's Bakehouse", label_visibility="collapsed")

    st.markdown('<div class="py-chip-label">Business type</div>', unsafe_allow_html=True)
    biz_type = st.radio("bt", ["Food & drink", "Retail / product", "Local services", "Fitness & wellness", "Other"],
                         horizontal=True, label_visibility="collapsed")

    st.markdown('<div class="py-chip-label">Main platform</div>', unsafe_allow_html=True)
    platform = st.radio("pl", ["Instagram", "TikTok", "YouTube Shorts", "Facebook"],
                         horizontal=True, label_visibility="collapsed")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="py-chip-label">Location</div>', unsafe_allow_html=True)
        location = st.text_input("loc", placeholder="e.g. Bengaluru, India", label_visibility="collapsed")
    with col2:
        st.markdown('<div class="py-chip-label">Revenue band</div>', unsafe_allow_html=True)
        revenue = st.selectbox("rv", ["Just starting out", "Steady, small team", "Established, growing"],
                                label_visibility="collapsed")

    st.write("")
    if st.button("Generate content idea →"):
        if not biz_name.strip():
            st.error("Enter a business name first.")
        else:
            st.session_state.biz = {
                "business_name": biz_name.strip(),
                "business_type": biz_type,
                "target_audience": st.session_state.description,
                "platform": platform,
                "location": location or "your city",
                "revenue_band": revenue,
            }
            st.session_state.stage = "results"
            st.rerun()

# ---------------------------------------------------------------- RESULTS
elif st.session_state.stage == "results":
    if st.button("← Start over"):
        st.session_state.stage = "landing"
        st.session_state.description = ""
        st.session_state.biz = {}
        st.rerun()

    status_map = {step: "pending" for step in STEP_ORDER}
    status_ph = st.empty()
    result_ph = st.empty()

    def render_status():
        rows = []
        for step in STEP_ORDER:
            s = status_map[step]
            dot_cls = s if s in ("running", "done") else ""
            rows.append(
                f'<div class="py-status-row {s}"><span class="py-status-dot {dot_cls}"></span>'
                f'<span>{STEP_LABELS[step]}</span></div>'
            )
        status_ph.markdown("".join(rows), unsafe_allow_html=True)

    render_status()

    try:
        with requests.post(f"{API_BASE}/api/content/stream", json=st.session_state.biz, stream=True, timeout=120) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data: "):
                    continue
                event = json.loads(line[len("data: "):])
                agent, status = event.get("agent"), event.get("status")

                if agent in STEP_ORDER:
                    status_map[agent] = "running" if status == "running" else "done"
                    render_status()

                if status == "complete":
                    script = event.get("output", {})
                    hashtags = " ".join(
                        f'<span class="py-tag-pill">{h}</span>' for h in script.get("hashtags", [])
                    )
                    shots = "".join(f"<li>{s}</li>" for s in script.get("shot_list", []))
                    result_ph.markdown(
                        f"""
                        <div class="py-result">
                            <div class="label">Hook</div><p>{script.get('hook','')}</p>
                            <div class="label">Shot list</div><ol>{shots}</ol>
                            <div class="label">Caption</div><p>{script.get('caption','')}</p>
                            <div class="label">Tags</div>{hashtags}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
    except requests.exceptions.ConnectionError:
        st.error(f"Couldn't reach the API at {API_BASE}. Is `uvicorn app.main:app --reload` running?")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")

# ---------------------------------------------------------------- ROADMAP THREAD (always visible, scroll down)
st.markdown('<div class="py-thread"><div class="py-thread-title">How it works</div>', unsafe_allow_html=True)

roadmap = [
    ("Tell us about your business", "Type it in above like you're describing it to a friend — no forms up front."),
    ("A few quick details", "Business type, platform, location, and revenue stage — five taps, not a survey."),
    ("We surface what's trending", "Matched to your industry and area, with a plain reason for every topic."),
    ("Get your content idea", "A hook, a shot list, and a caption — written for your business, ready to film."),
]
for i, (title, body) in enumerate(roadmap, start=1):
    st.markdown(
        f'<div class="py-step-row"><div class="py-step-num">{i}</div>'
        f'<div class="py-step-body"><h4>{title}</h4><p>{body}</p></div></div>',
        unsafe_allow_html=True,
    )
st.markdown('</div>', unsafe_allow_html=True)
