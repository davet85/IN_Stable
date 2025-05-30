# main.py

import streamlit as st
import datetime
from gpt.gpt_handler import handle_prompt
from core.memory.session_memory import load_session_memory, save_session_memory
from core.memory.memory_engine import calculate_alignment_score
from utils.logger import log_info, log_error

# --- UI Setup
st.set_page_config(page_title="Loop – Reflect to Evolve", layout="wide")
st.title("🔁 Loop")
st.subheader("Realign. Reflect. Evolve.")

# --- Load Memory and State
memory = load_session_memory()
st.session_state.setdefault("badges", [])
st.session_state.setdefault("active_champion", "Observer")

# --- Level System
def get_user_level(score: float) -> int:
    thresholds = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95]
    for i, threshold in enumerate(thresholds, 1):
        if score < threshold:
            return i
    return 10

# --- Input Section
user_input = st.text_area("💬 Enter a thought, observation, or reflection", height=150)
tag_input = st.text_input("🏷️ Optional Tag (e.g., #insight, #loop, #trigger)")

col1, col2 = st.columns(2)
with col1:
    submit = st.button("📤 Submit to Loop")
with col2:
    show_history = st.checkbox("📚 Show Session History")

# --- Submission Logic
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
            st.success("🧠 Loop Reflection:")
            st.markdown(f"> {response}")

            # --- Badge Trigger Example
            if "#mask" in tag_input.lower() and "Mask" not in st.session_state.badges:
                st.session_state.badges.append("Mask")
                st.toast("🏅 New badge earned: Mask")

        except Exception as e:
            log_error(f"Error handling input: {str(e)}")
            st.error(f"Something went wrong: {str(e)}")

# --- RCA Scoring + Level Display
if memory:
    score = calculate_alignment_score(memory)
    level = get_user_level(score)

    st.sidebar.subheader("📈 RCA Alignment Score")
    st.sidebar.metric(label="Score", value=f"{score:.2f} / 1.0")
    st.sidebar.subheader("🧩 Loop Level")
    st.sidebar.metric(label="Level", value=f"{level}/10")

    if level >= 5:
        st.balloons()
        st.success("🎉 You've leveled up your cognitive evolution!")

# --- Unlockables (Themes + Champions)
st.markdown("## 🏅 Unlock Progress")

badge_count = len(st.session_state.badges)
unlockables = [
    {"name": "Theme: Clarity", "required": 2},
    {"name": "Champion: Guardian", "required": 3},
    {"name": "Theme: Focus", "required": 4},
    {"name": "Champion: Architect", "required": 5},
    {"name": "Theme: Guilt", "required": 6},
    {"name": "Champion: Witness", "required": 7},
    {"name": "Theme: Identity", "required": 8},
    {"name": "Champion: Catalyst", "required": 9},
]

for unlock in unlockables:
    progress = min(badge_count / unlock["required"], 1.0)
    status = "✅" if badge_count >= unlock["required"] else "🔒"
    st.markdown(f"**{status} {unlock['name']}**")
    st.progress(progress)

# --- Champion Avatar Selector
st.markdown("## 🧙 Choose Your Champion")

champion_unlocks = {
    "Guardian": 3,
    "Architect": 5,
    "Witness": 7,
    "Catalyst": 9
}
unlocked_champions = ["Observer"] + [
    champ for champ, required in champion_unlocks.items() if badge_count >= required
]

default_index = unlocked_champions.index(st.session_state["active_champion"]) \
    if st.session_state["active_champion"] in unlocked_champions else 0
selected = st.selectbox("Select your current champion:", unlocked_champions, index=default_index)
st.session_state["active_champion"] = selected
st.info(f"🧭 Current Champion: **{selected}**")

# --- Session Timeline Viewer
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
