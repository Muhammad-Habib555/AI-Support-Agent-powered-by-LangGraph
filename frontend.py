import streamlit as st
import requests

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(page_title="🧠 AI Support Agent", layout="centered")
st.title("🧠 AI Support Agent")

# ----------------------------
# Sidebar for options
# ----------------------------
with st.sidebar:
    st.header("Options")
    if st.button("➕ New Chat"):
        # Reset session memory
        st.session_state.messages = []
        st.session_state.last_response = ""
        st.session_state.last_res_data = {}
    st.markdown("---")
    st.caption("LangGraph + Structured Output")
    st.caption("FastAPI backend")

# ----------------------------
# Initialize session state
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_response" not in st.session_state:
    st.session_state.last_response = ""

if "last_res_data" not in st.session_state:
    st.session_state.last_res_data = {}

# ----------------------------
# Display full conversation
# ----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------
# User input
# ----------------------------
user_input = st.chat_input("Type your message...")
if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # ----------------------------
    # Send to backend
    # ----------------------------
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://localhost:8000/support",
                    json={"messages": st.session_state.messages},
                    timeout=60,
                )
                response.raise_for_status()
                data = response.json()

                assistant_reply = data.get(
                    "final_response", "Sorry, something went wrong."
                )
                st.session_state.last_response = assistant_reply
                st.session_state.last_res_data = data
            except Exception as e:
                assistant_reply = f"Error: {e}"

            # Display assistant message
            st.markdown(assistant_reply)
            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_reply}
            )

# ----------------------------
# Conversation info
# ----------------------------
with st.expander("Conversation Info"):
    st.write(f"Total messages: {len(st.session_state.messages)}")
    if st.session_state.last_res_data:
        st.write(f"Intent: {st.session_state.last_res_data.get('intent')}")
        st.write(f"Sentiment: {st.session_state.last_res_data.get('sentiment')}")
        st.write(
            f"Needs Escalation: {st.session_state.last_res_data.get('needs_escalation')}"
        )
