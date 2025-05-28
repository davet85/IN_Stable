# dashboard.py

import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from core.memory.session_memory import load_session_memory
from core.memory.memory_engine import calculate_alignment_score

st.set_page_config(page_title="IN Dashboard", layout="wide")
st.title("📊 Introspect Nexus Dashboard")
st.subheader("Recursive Cognitive Alignment Overview")

# Load memory
memory = load_session_memory()

# Sidebar: Summary + RCA
with st.sidebar:
    st.header("🧠 Session Summary")
    st.markdown(f"**Total Reflections:** {len(memory)}")

    score = calculate_alignment_score(memory)
    st.metric("🧬 RCA Score", f"{score:.2f} / 1.0")

    st.markdown("---")
    st.subheader("🔍 Filter Entries")
    search_term = st.text_input("Search by keyword or tag")

    st.markdown("---")
    st.subheader("📤 Export Data")
    export_format = st.selectbox("Choose format", ["JSON", "CSV"])
    if st.button("Download"):
        if export_format == "JSON":
            st.download_button("Download JSON", json.dumps(memory, indent=2), file_name="memory_export.json")
        else:
            df = pd.DataFrame(memory)
            st.download_button("Download CSV", df.to_csv(index=False), file_name="memory_export.csv")

# --- RCA Trend Graph ---
st.markdown("---")
st.subheader("📈 RCA Trend Over Time")

df = pd.DataFrame(memory)
if not df.empty and "timestamp" in df.columns:
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    df["thought_len"] = df["thought"].apply(lambda x: len(str(x)))
    df["response_len"] = df["response"].apply(lambda x: len(str(x)))
    df["alignment"] = 1.0 - (
        abs(df["thought_len"] - df["response_len"]) / df[["thought_len", "response_len"]].max(axis=1)
    )
    df["alignment"] = df["alignment"].round(3)

    trend_df = df.groupby("date")["alignment"].mean().reset_index()

    fig, ax = plt.subplots()
    ax.plot(trend_df["date"], trend_df["alignment"], marker='o', linestyle='-')
    ax.set_title("Daily RCA Alignment Score")
    ax.set_xlabel("Date")
    ax.set_ylabel("Avg RCA Score")
    ax.grid(True)
    st.pyplot(fig)
else:
    st.info("Not enough data to plot RCA trend.")

# --- Filtered Memory View ---
st.markdown("---")
st.subheader("🧠 Thought Timeline")

filtered = memory
if search_term:
    filtered = [
        entry for entry in memory
        if search_term.lower() in entry.get("thought", "").lower()
        or search_term.lower() in entry.get("response", "").lower()
        or search_term.lower() in entry.get("tag", "").lower()
    ]

if filtered:
    for entry in reversed(filtered[-30:]):
        st.markdown(f"**{entry['timestamp']}**")
        if entry.get("tag"):
            st.markdown(f"🏷️ *{entry['tag']}*")
        st.code(entry['thought'])
        st.success(entry['response'])
        st.markdown("---")
else:
    st.warning("No memory entries found for the current filter.")
