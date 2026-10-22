import requests
import streamlit as st

# API URL comes from Streamlit Secrets on the cloud, localhost when running locally
try:
    API_URL = st.secrets["API_URL"]
except Exception:
    API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Student Predictor",
    page_icon="🌌",
    layout="centered",
)

# ---------- State (decides which theme we show) ----------
if "state" not in st.session_state:
    st.session_state.state = "idle"  # idle | pass | fail
    st.session_state.result = None
    st.session_state.error = None
    st.session_state.celebrate = False


def reset_theme():
    """Called when a slider moves: go back to the galaxy."""
    st.session_state.state = "idle"
    st.session_state.result = None
    st.session_state.error = None


def run_prediction():
    """Called when the button is clicked (runs before the page reruns)."""
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={
                "study_hours": st.session_state.study_hours,
                "prev_score": st.session_state.prev_score,
            },
            headers={"ngrok-skip-browser-warning": "true"},
            timeout=30,
        )
    except requests.exceptions.RequestException:
        reset_theme()
        st.session_state.error = (
            "Could not reach the prediction API. Is FastAPI and ngrok running?"
        )
        return

    if response.status_code != 200:
        reset_theme()
        st.session_state.error = f"API returned an error (status {response.status_code})."
        return

    result = response.json()
    st.session_state.result = result
    st.session_state.error = None

    if result["prediction"] == 1:
        st.session_state.state = "pass"
        st.session_state.celebrate = True
    else:
        st.session_state.state = "fail"


# ---------- Themes ----------
THEMES = {
    "idle": {
        "accent": "#b388ff",
        "accent2": "#4dd0ff",
        "base": "radial-gradient(ellipse at 20% 10%, #2b1055 0%, transparent 55%), "
                "radial-gradient(ellipse at 80% 90%, #0b3a75 0%, transparent 55%), #05010f",
        "blobs": "radial-gradient(circle at 25% 30%, rgba(179,136,255,0.45), transparent 40%), "
                 "radial-gradient(circle at 75% 65%, rgba(77,208,255,0.35), transparent 40%), "
                 "radial-gradient(circle at 50% 90%, rgba(255,105,180,0.30), transparent 35%)",
        "stars": "1",
        "speed": "18s",
        "hue": "25deg",
        "icon": "🌌",
        "sub": "Slide the values, hit predict, and let the galaxy decide",
        "emoji": "",
    },
    "pass": {
        "accent": "#00ffa3",
        "accent2": "#5cffd9",
        "base": "linear-gradient(160deg, #011a17 0%, #02221c 50%, #01100f 100%)",
        "blobs": "radial-gradient(ellipse at 20% 20%, rgba(0,255,163,0.55), transparent 45%), "
                 "radial-gradient(ellipse at 80% 35%, rgba(0,229,255,0.40), transparent 45%), "
                 "radial-gradient(ellipse at 50% 75%, rgba(120,255,120,0.35), transparent 45%), "
                 "radial-gradient(ellipse at 90% 85%, rgba(160,100,255,0.25), transparent 40%)",
        "stars": "0.5",
        "speed": "9s",
        "hue": "40deg",
        "icon": "🌟",
        "sub": "Northern lights are on, you're going to shine",
        "emoji": "🎉",
    },
    "fail": {
        "accent": "#ff3b5c",
        "accent2": "#ff8a9b",
        "base": "linear-gradient(160deg, #1c0209 0%, #3a0616 55%, #14010a 100%)",
        "blobs": "radial-gradient(circle at 25% 25%, rgba(190,20,60,0.50), transparent 42%), "
                 "radial-gradient(circle at 78% 70%, rgba(120,10,45,0.60), transparent 45%), "
                 "radial-gradient(circle at 50% 95%, rgba(255,60,90,0.25), transparent 35%)",
        "stars": "0.15",
        "speed": "14s",
        "hue": "0deg",
        "icon": "🍷",
        "sub": "Not this time. A bit more study can change it",
        "emoji": "🥀",
    },
}

state = st.session_state.state
t = THEMES[state]

# Theme variables (these change with the state)
st.markdown(
    f"""
<style>
:root {{
    --accent: {t['accent']};
    --accent2: {t['accent2']};
    --base: {t['base']};
    --blobs: {t['blobs']};
    --stars: {t['stars']};
    --speed: {t['speed']};
    --hue: {t['hue']};
}}
</style>
""",
    unsafe_allow_html=True,
)

# Static CSS (same for every theme, uses the variables above)
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }

/* ----- Animated background ----- */
[data-testid="stAppViewContainer"] { background: var(--base); }

/* Moving colour clouds (nebula / aurora / wine glow) */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed; inset: -20%;
    z-index: 0; pointer-events: none;
    background: var(--blobs);
    filter: blur(55px);
    animation: drift var(--speed) ease-in-out infinite alternate, themeIn 1.2s ease both;
}

/* Twinkling stars */
[data-testid="stAppViewContainer"]::after {
    content: "";
    position: fixed; inset: 0;
    z-index: 0; pointer-events: none;
    opacity: var(--stars);
    background-image:
        radial-gradient(1.5px 1.5px at 20px 30px, #fff, transparent),
        radial-gradient(1px 1px at 120px 90px, #dfe9ff, transparent),
        radial-gradient(2px 2px at 170px 160px, #fff, transparent),
        radial-gradient(1px 1px at 60px 170px, #fff, transparent),
        radial-gradient(1.5px 1.5px at 210px 40px, #cfe0ff, transparent),
        radial-gradient(1px 1px at 90px 230px, #fff, transparent);
    background-size: 250px 250px;
    animation: twinkle 4s ease-in-out infinite alternate;
}

/* Keep real content above the background layers */
[data-testid="stMain"], .block-container { position: relative; z-index: 1; }
.block-container { max-width: 760px; padding-top: 2.5rem; }

/* ----- Keyframes ----- */
@keyframes drift {
    0%   { transform: translate(-4%, -3%) scale(1);    filter: blur(55px) hue-rotate(0deg); }
    100% { transform: translate(4%, 3%)  scale(1.15); filter: blur(55px) hue-rotate(var(--hue)); }
}
@keyframes twinkle {
    0%   { opacity: var(--stars); }
    100% { opacity: calc(var(--stars) * 0.35); }
}
@keyframes themeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes shine {
    0%   { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 20px var(--accent); }
    50%      { box-shadow: 0 0 48px var(--accent); }
}
@keyframes grow { from { width: 0; } }
@keyframes floaty {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-9px); }
}

/* ----- Hero ----- */
.hero { text-align: center; animation: fadeUp 0.8s ease both; margin-bottom: 1.5rem; }
.hero .icon { font-size: 3.4rem; display: inline-block; animation: floaty 3s ease-in-out infinite; }
.hero h1 {
    font-size: 2.4rem; font-weight: 700; margin: 0.2rem 0;
    background: linear-gradient(90deg, var(--accent), #ffffff, var(--accent2), var(--accent));
    background-size: 200% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: shine 5s linear infinite;
}
.hero p { color: #d6d3ef; font-weight: 300; }

/* ----- Glass card around the sliders ----- */
.st-key-inputs {
    background: rgba(255, 255, 255, 0.07);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 22px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45);
    padding: 1.2rem 1rem;
    animation: fadeUp 0.9s ease both;
}
[data-testid="stWidgetLabel"] p { color: #efeaff !important; font-weight: 600; }
[data-baseweb="slider"] div[role="slider"] { background-color: var(--accent) !important; }
[data-testid="stSliderThumbValue"] { color: var(--accent) !important; }

/* ----- Button ----- */
div.stButton > button {
    width: 100%;
    border: none;
    border-radius: 14px;
    padding: 0.85rem 1rem;
    font-size: 1.05rem;
    font-weight: 700;
    color: #07040f;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    animation: fadeUp 1s ease both;
}
div.stButton > button:hover {
    transform: translateY(-3px) scale(1.01);
    box-shadow: 0 10px 30px var(--accent);
    color: #07040f;
}
div.stButton > button:active { transform: scale(0.98); color: #07040f; }

/* ----- Result card ----- */
.result {
    margin-top: 1.4rem; padding: 1.6rem; border-radius: 22px; text-align: center;
    background: rgba(255, 255, 255, 0.07);
    backdrop-filter: blur(14px);
    border: 1px solid var(--accent);
    animation: fadeUp 0.6s ease both, pulseGlow 2.5s ease-in-out infinite;
}
.result .label { color: #cfcbe8; font-size: 0.9rem; letter-spacing: 2px; text-transform: uppercase; }
.result .verdict { font-size: 3rem; font-weight: 700; margin: 0.2rem 0 1rem; color: var(--accent); }
.bar-bg { height: 12px; background: rgba(255, 255, 255, 0.12); border-radius: 99px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, var(--accent), var(--accent2)); animation: grow 1.2s ease both; }
.result .conf { color: #efeaff; margin-top: 0.6rem; font-size: 0.95rem; }

/* ----- Summary chips ----- */
.chips { display: flex; gap: 1rem; margin-top: 1.6rem; animation: fadeUp 1.1s ease both; }
.chip {
    flex: 1; text-align: center; padding: 1rem; border-radius: 16px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.14);
    transition: transform 0.25s ease, border-color 0.25s ease;
}
.chip:hover { transform: translateY(-5px); border-color: var(--accent); }
.chip .k { color: #cfcbe8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px; }
.chip .v { color: var(--accent); font-size: 1.6rem; font-weight: 700; }

/* ----- Expander ----- */
[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 14px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Hero ----------
st.markdown(
    f"""
<div class="hero">
    <div class="icon">{t['icon']}</div>
    <h1>Student Pass / Fail Predictor</h1>
    <p>{t['sub']}</p>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- Inputs ----------
with st.container(key="inputs"):
    col1, col2 = st.columns(2)
    with col1:
        study_hours = st.slider(
            "📚 Study Hours Per Day",
            min_value=0.0,
            max_value=10.0,
            value=4.0,
            step=0.5,
            key="study_hours",
            on_change=reset_theme,
            help="How many hours the student studies each day",
        )
    with col2:
        prev_score = st.slider(
            "📝 Previous Exam Score",
            min_value=0.0,
            max_value=100.0,
            value=60.0,
            step=1.0,
            key="prev_score",
            on_change=reset_theme,
            help="Score from the most recent exam (out of 100)",
        )

st.write("")

# ---------- Predict button ----------
st.button("✨ Predict Result", on_click=run_prediction)

# ---------- Output ----------
if st.session_state.error:
    st.error(st.session_state.error)

result = st.session_state.result
if result:
    pct = result["confidence"] * 100
    st.markdown(
        f"""
<div class="result">
    <div class="label">Prediction</div>
    <div class="verdict">{t['emoji']} {result['result_label']}</div>
    <div class="bar-bg"><div class="bar-fill" style="width: {pct:.1f}%;"></div></div>
    <div class="conf">Model confidence: <b>{pct:.1f}%</b></div>
</div>
""",
        unsafe_allow_html=True,
    )

    if st.session_state.celebrate:
        st.balloons()
        st.session_state.celebrate = False

    with st.expander("🔍 See what was sent to the API"):
        st.json({"study_hours": study_hours, "prev_score": prev_score})
        st.json(result)

# ---------- Live summary ----------
st.markdown(
    f"""
<div class="chips">
    <div class="chip"><div class="k">Study Hours</div><div class="v">{study_hours} hrs</div></div>
    <div class="chip"><div class="k">Previous Score</div><div class="v">{prev_score:.0f}/100</div></div>
</div>
""",
    unsafe_allow_html=True,
)