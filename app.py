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

/* Page background */
.stApp { background-color: #FDF6EC; }
[data-testid="stAppViewContainer"] { background-color: #FDF6EC; }
[data-testid="stHeader"] { background-color: #FDF6EC; }

/* Header icons visibility (toggle + menu) */
[data-testid="stHeader"] button,
[data-testid="stHeader"] svg,
[data-testid="collapsedControl"] svg {
    color:#000 !important;
    fill:#000 !important;
    opacity:1 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color:#FFF3DC;
    border-right:2px solid #E8C97A;
}

/* Sidebar buttons (UNCHANGED aesthetic) */
[data-testid="stSidebar"] .stButton button {
    background-color:#FDF6EC;
    color:#7A3B00;
    border:1px solid #E07B00;
    border-radius:8px;
    text-align:left;
    font-size:0.85rem;
    padding:0.4rem 0.7rem;
    width:100%;
}
[data-testid="stSidebar"] .stButton button:hover {
    background-color:#FFE4A0;
    border-color:#C47A2B;
}

/* Header text */
.paatti-header {
    text-align:center;
    padding:1.5rem 0 0.8rem 0;
}
.paatti-header h1 {
    font-family:'Noto Serif', Georgia, serif;
    color:#7A3B00;
    font-size:2.4rem;
}
.paatti-header .tamil-sub {
    font-size:1.15rem;
    color:#C47A2B;
    font-style:italic;
}
.paatti-header .tagline {
    font-size:0.92rem;
    color:#8B6343;
}

/* Divider */
hr {
    border:none;
    border-top:1px solid #E8C97A;
}

/* Chat messages */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background-color:#FFF8EE;
    border:1px solid #F0D9A0;
    border-radius:14px;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background-color:#F0F4FF;
    border:1px solid #C5CFF0;
    border-radius:14px;
}

/* Chat input */
[data-testid="stChatInput"] {
    border-top:2px solid #E8C97A;
    background-color:#FDF6EC;
}
[data-testid="stChatInput"] textarea {
    background-color:#FFFBF4 !important;
    border:1.5px solid #E07B00 !important;
    border-radius:24px !important;
    color:#3D1F00 !important;
    caret-color:#000 !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color:#C47A2B !important;
    box-shadow:0 0 0 2px rgba(196,122,43,0.15) !important;
}

/* Message text */
[data-testid="stChatMessageContent"] p {
    color:#2C1A00;
}

/* Spinner */
.stSpinner > div {
    border-top-color:#E07B00 !important;
}

/* ───── SAFE VISIBILITY PATCH (NO DESIGN CHANGE) ───── */
textarea, input {
    caret-color:#7A3B00 !important;
}
button svg {
    opacity:1 !important;
    visibility:visible !important;
}
button {
    opacity:1;
}
textarea::placeholder {
    opacity:0.8;
}
textarea:focus, button:focus {
    outline:none;
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
    st.markdown("<h3 style='color:#7A3B00;'>💬 Ask Paatti about...</h3>", unsafe_allow_html=True)

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

    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── Chat history ──────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role":"assistant",
        "content":"வணக்கம் Kanna! 🙏\n\nI am Avvaiyar Paatti..."
    }]

for msg in st.session_state.messages:
    avatar = "👵" if msg["role"]=="assistant" else "🧑"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

prefill = st.session_state.pop("prefill", None)
user_input = st.chat_input("Tell Paatti what's on your mind...") or prefill

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="👵"):
        placeholder = st.empty()
        with st.spinner("Paatti is thinking... 🤔"):
            try:
                resp = requests.post(API_URL,json={"query":user_input},timeout=60)

                if resp.status_code==200:
                    bot_text = resp.json().get("response","")
                    displayed=""
                    for word in bot_text.split():
                        displayed += word+" "
                        placeholder.markdown(displayed+"▌")
                        time.sleep(0.03)

                    placeholder.markdown(displayed.strip())
                    st.session_state.messages.append({
                        "role":"assistant",
                        "content":displayed.strip()
                    })

                elif resp.status_code==503:
                    placeholder.warning("Paatti is waking up — try again 🙏")
                else:
                    placeholder.error(f"Error {resp.status_code}")

            except Exception as e:
                placeholder.error(str(e))
