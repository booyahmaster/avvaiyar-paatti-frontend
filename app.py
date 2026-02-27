import streamlit as st
import requests
import time

# ── Page config ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Avvaiyar Paatti AI",
    page_icon="👵",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Styling ───────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,400;0,700;1,400&display=swap');

    /* ── Base page ── */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"] {
        background-color: #FDF6EC !important;
    }

    /* ── Sidebar background ── */
    [data-testid="stSidebar"] {
        background-color: #FFF3DC !important;
        border-right: 2px solid #E8C97A;
    }

    /* ── Sidebar heading text ── */
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #4A2000;
    }

    /* ══════════════════════════════════════════════
       SIDEBAR EXAMPLE BUTTONS  — HIGH CONTRAST FIX
    ══════════════════════════════════════════════ */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #C47A2B !important;      /* warm amber */
        color: #FFFFFF !important;                 /* pure white text — always visible */
        border: 1.5px solid #A05A10 !important;
        border-radius: 10px !important;
        text-align: left !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 0.45rem 0.8rem !important;
        width: 100% !important;
        margin-bottom: 3px !important;
        transition: background-color 0.18s, transform 0.1s !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.15) !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #A05A10 !important;
        transform: translateX(2px) !important;
        border-color: #7A3B00 !important;
    }

    [data-testid="stSidebar"] .stButton > button:active {
        background-color: #7A3B00 !important;
        transform: translateX(0px) !important;
    }

    /* ══════════════════════════════════════════════
       CLEAR CHAT BUTTON  — DISTINCT RED VARIANT
    ══════════════════════════════════════════════ */
    [data-testid="stSidebar"] .stButton > button[kind="secondary"],
    [data-testid="stSidebar"] .stButton:last-of-type > button {
        background-color: #B03A2E !important;      /* deep red */
        color: #FFFFFF !important;
        border: 1.5px solid #8B2020 !important;
        margin-top: 4px !important;
    }
    [data-testid="stSidebar"] .stButton:last-of-type > button:hover {
        background-color: #8B2020 !important;
    }

    /* ══════════════════════════════════════════════
       HEADER ICONS — minimal, non-destructive fix
    ══════════════════════════════════════════════ */
    header[data-testid="stHeader"] svg,
    header[data-testid="stHeader"] path {
        fill: #7A3B00 !important;
        stroke: #7A3B00 !important;
    }

    /* ── Page header ── */
    .paatti-header {
        text-align: center;
        padding: 1.5rem 0 0.8rem 0;
    }
    .paatti-header h1 {
        font-family: 'Noto Serif', Georgia, serif;
        color: #7A3B00;
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }
    .paatti-header .tamil-sub {
        font-size: 1.15rem;
        color: #C47A2B;
        font-style: italic;
        margin-bottom: 0.3rem;
    }
    .paatti-header .tagline {
        font-size: 0.92rem;
        color: #8B6343;
    }

    /* ── Divider ── */
    hr {
        border: none;
        border-top: 1px solid #E8C97A;
        margin: 0.5rem 0 1rem 0;
    }

    /* ── Chat bubbles — assistant ── */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background-color: #FFF8EE;
        border: 1px solid #F0D9A0;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
    }

    /* ── Chat bubbles — user ── */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background-color: #F0F4FF;
        border: 1px solid #C5CFF0;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
    }

    /* ── Chat input box ── */
    [data-testid="stChatInput"] {
        border-top: 2px solid #E8C97A;
        background-color: #FDF6EC;
        padding-top: 0.5rem;
    }
    [data-testid="stChatInput"] textarea {
        background-color: #FFFBF4 !important;
        border: 1.5px solid #E07B00 !important;
        border-radius: 24px !important;
        color: #3D1F00 !important;
        caret-color: #3D1F00 !important;
        font-size: 0.97rem !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #C47A2B !important;
        box-shadow: 0 0 0 2px rgba(196, 122, 43, 0.15) !important;
    }

    /* ── Message text ── */
    [data-testid="stChatMessageContent"] p {
        font-size: 1rem;
        line-height: 1.65;
        color: #2C1A00;
    }

    /* ── Spinner ── */
    .stSpinner > div {
        border-top-color: #E07B00 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Backend URL ───────────────────────────────────────────────────
API_URL = st.secrets.get("API_URL", "https://GSR-608001-avvaiyar-brain.hf.space/chat")

# ── Header ────────────────────────────────────────────────────────
st.markdown("""
<div class="paatti-header">
    <h1>👵 Avvaiyar Paatti AI</h1>
    <div class="tamil-sub">ஔவையார் பாட்டி</div>
    <div class="tagline">Ancient Tamil wisdom for modern life — ask me anything</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h3 style='color:#7A3B00; font-size:1rem; margin-bottom:0.5rem;'>💬 Ask Paatti about...</h3>", unsafe_allow_html=True)
    examples = [
        "I keep procrastinating my work",
        "My friend betrayed my trust",
        "I am losing motivation to study",
        "How do I deal with an arrogant person?",
        "I want to succeed but feel lost",
        "I feel lazy and unmotivated",
        "I get angry very easily",
        "I lied to someone I care about",
        "I feel jealous of others' success",
        "I never appreciate what I have",
    ]
    for ex in examples:
        if st.button(ex, key=ex, use_container_width=True):
            st.session_state["prefill"] = ex

    st.divider()
    st.markdown("""
    <div style='font-size:0.78rem; color:#5A3000; line-height:1.6;'>
    <b>About</b><br>
    Avvaiyar Paatti gives life advice rooted in the 2,000-year-old Tamil text <i>Aathichoodi</i> by poet Avvaiyar.<br><br>
    <b>Stack</b><br>
    Fine-tuned Embeddings · FAISS · Gemini 2.0 Flash · FastAPI · Streamlit
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── Chat history ──────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "வணக்கம் Kanna! 🙏\n\nI am Avvaiyar Paatti. \n\nThe ancient wisdom of Aathichoodi has guided hearts for 2,000 years. What is on your mind today?"
    })

# Display history
for msg in st.session_state.messages:
    avatar = "👵" if msg["role"] == "assistant" else "🧑"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ── Handle sidebar button prefill ────────────────────────────────
prefill = st.session_state.pop("prefill", None)

# ── Chat input ────────────────────────────────────────────────────
user_input = st.chat_input("Tell Paatti what's on your mind...") or prefill

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="👵"):
        placeholder = st.empty()
        with st.spinner("Paatti is thinking... 🤔"):
            try:
                resp = requests.post(
                    API_URL,
                    json={"query": user_input},
                    timeout=60,
                )
                if resp.status_code == 200:
                    bot_text = resp.json().get("response", "")

                    # Word-by-word streaming effect
                    displayed = ""
                    for word in bot_text.split():
                        displayed += word + " "
                        placeholder.markdown(displayed + "▌")
                        time.sleep(0.03)
                    placeholder.markdown(displayed.strip())

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": displayed.strip(),
                    })

                elif resp.status_code == 503:
                    placeholder.warning("Paatti is waking up — please send your message again in a few seconds 🙏")
                else:
                    placeholder.error(f"Something went wrong (error {resp.status_code}). Please try again.")

            except requests.exceptions.Timeout:
                placeholder.error("Took too long. Please try again — Paatti is still here 🙏")
            except requests.exceptions.ConnectionError:
                placeholder.error("Cannot reach the backend. Please check if the HF Space is running.")
            except Exception as e:
                placeholder.error(f"Unexpected error: {str(e)}")
