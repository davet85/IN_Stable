# main.py

import streamlit as st
import datetime
from gpt.gpt_handler import handle_prompt
from core.memory.session_memory import load_session_memory, save_session_memory
from core.memory.memory_engine import calculate_alignment_score
from utils.logger import log_info, log_error

st.set_page_config(page_title="Introspect Nexus", layout="wide")
st.title("🧠 Introspect Nexus")
st.subheader("Realign. Reflect. Refine.")

# --- Load existing memory
memory = load_session_memory()

# --- User input
user_input = st.text_area("💬 Enter a thought, observation, or reflection", height=150)
tag_input = st.text_input("🏷️ Optional Tag (e.g., #insight, #loop, #trigger)")

col1, col2 = st.columns(2)
with col1:
    submit = st.button("📤 Submit to GPT")
with col2:
    show_history = st.checkbox("📚 Show Session History")

# --- Submission flow
if submit:
    if not user_input.strip():
        st.warning("Please enter a prompt.")
    else:
        try:
            response = handle_prompt(user_input)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = {
                "timestamp": timestamp,
                "thought": user_input.strip(),
                "response": response,
                "tag": tag_input.strip()
            }
            memory.append(entry)
            save_session_memory(memory)
            log_info("Thought submitted and saved.")
            st.success("🧠 GPT Response:")
            st.markdown(f"> {response}")
        except Exception as e:
            log_error(f"Error handling input: {str(e)}")
            st.error(f"Something went wrong: {str(e)}")

# --- RCA score
if memory:
    score = calculate_alignment_score(memory)
    st.sidebar.subheader("📈 RCA Alignment Score")
    st.sidebar.metric(label="Score", value=f"{score:.2f} / 1.0")

# --- Optional history viewer
if show_history and memory:
    st.markdown("---")
    st.subheader("📜 Session Timeline")
    for entry in reversed(memory[-10:]):
        st.markdown(f"**{entry['timestamp']}**")
        if entry.get("tag"):
            st.markdown(f"🏷️ *{entry['tag']}*")
        st.code(f"🗯️ {entry['thought']}")
        st.success(f"🔁 {entry['response']}")
        st.markdown("---")
