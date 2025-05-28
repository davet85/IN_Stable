import streamlit as st
import os
import json
import datetime
from core.memory.session_memory import load_session_memory
from core.memory.memory_engine import calculate_alignment_score  # Stub
from gpt.gpt_handler import handle_prompt

st.set_page_config(page_title="IN Dashboard", layout="wide")
st.title("📊 Introspect Nexus: Cognitive Alignment Dashboard")

# --- Load Memory
memory_data = load_session_memory()

# --- Sidebar: Session Info
with st.sidebar:
    st.header("🧠 Session Overview")
    st.markdown(f"**Total Thoughts Recorded:** {len(memory_data)}")
    
    if memory_data:
        latest = memory_data[-1]
        st.markdown(f"**Last Entry:** {latest.get('timestamp', 'N/A')}")
        st.markdown(f"**Last Thought:** {latest.get('thought', 'N/A')[:75]}...")

    st.markdown("---")
    st.subheader("📈 RCA Alignment")
    st.write("*(Scoring based on concept coherence – stub)*")
    score = calculate_alignment_score(memory_data) if memory_data else 0
    st.metric("Alignment Score", f"{score:.2f} / 1.0")

# --- Main Panel: Timeline Viewer
st.subheader("🧭 Thought Timeline")

if memory_data:
    for entry in reversed(memory_data):
        st.markdown(f"**{entry['timestamp']}**")
        st.code(f"🗯️ {entry['thought']}")
        st.success(f"🔁 {entry['response']}")
        st.markdown("---")
else:
    st.warning("No session data found.")

# --- User Input for Live Submission
st.subheader("➕ Submit New Reflection")

new_thought = st.text_area("Enter a thought or question")
if st.button("Submit to GPT"):
    if new_thought:
        response = handle_prompt(new_thought)
        st.markdown("**Response:**")
        st.success(response)

        # Save to memory
        from core.memory.session_memory import save_session_memory
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = {"timestamp": now, "thought": new_thought, "response": response}
        memory_data.append(new_entry)
        save_session_memory(memory_data)
    else:
        st.warning("Thought input is empty.")
