import streamlit as st
from openai import OpenAI

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Advanced AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ================= CUSTOM STYLE =================
st.markdown("""
<style>
.chat-box {max-width: 800px; margin: auto;}
</style>
""", unsafe_allow_html=True)

st.title("🤖 Advanced AI Chatbot")
st.caption("Memory • Smart Replies • Streamlit")

# ================= OPENAI CLIENT =================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ================= SYSTEM PROMPT =================
SYSTEM_PROMPT = """
You are an advanced AI assistant.
You reply in a clear, helpful, and professional way.
If user mixes Urdu and English, respond in both.
Explain things step by step when needed.
"""

# ================= SESSION MEMORY =================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# ================= CLEAR CHAT =================
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    st.experimental_rerun()

# ================= DISPLAY CHAT =================
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ================= USER INPUT =================
user_input = st.chat_input("Ask anything...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        temperature=0.7
    )

    reply = response.choices[0].message.content

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.markdown(reply)
