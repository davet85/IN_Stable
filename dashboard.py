import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from core.memory.session_memory import load_session_memory
from core.memory.memory_engine import calculate_alignment_score
from core.memory.cluster_engine import cluster_thoughts, generate_cluster_label

st.set_page_config(page_title="IN Dashboard", layout="wide")
st.title("📊 Introspect Nexus Dashboard")
st.subheader("Recursive Cognitive Alignment Overview")

# Load session memory
memory = load_session_memory()
if not memory or not isinstance(memory, list):
    st.error("❌ Failed to load session memory.")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("🧠 Session Summary")
    st.markdown(f"**Total Reflections:** {len(memory)}")

    try:
        score = calculate_alignment_score(memory)
        st.metric("🧬 RCA Score", f"{score:.2f} / 1.0")
    except Exception as e:
        st.error(f"RCA score error: {e}")
        score = 0.0

    st.markdown("---")
    st.subheader("🔍 Search & Filter")
    search_term = st.text_input("Search by keyword or tag")
    filter_type = st.radio("Filter in:", ["All", "Thoughts", "Responses", "Tags"], horizontal=True)

    def entry_matches(entry):
        term = search_term.lower()
        if filter_type == "All":
            return term in entry.get("thought", "").lower() or \
                   term in entry.get("response", "").lower() or \
                   term in entry.get("tag", "").lower()
        return term in entry.get(filter_type.lower(), "").lower()

    filtered_memory = [entry for entry in memory if entry_matches(entry)] if search_term else memory

    st.markdown("---")
    st.subheader("📤 Export Data")
    export_format = st.selectbox("Choose format", ["JSON", "CSV"])
    if st.button("Download"):
        if export_format == "JSON":
            st.download_button("Download JSON", data=json.dumps(filtered_memory, indent=2),
                               file_name="memory_export.json", mime="application/json")
        else:
            df_export = pd.DataFrame(filtered_memory)
            st.download_button("Download CSV", data=df_export.to_csv(index=False),
                               file_name="memory_export.csv", mime="text/csv")

# RCA Trend Over Time
st.markdown("---")
st.subheader("📈 RCA Trend Over Time")
df = pd.DataFrame(memory)

if not df.empty and "timestamp" in df.columns:
    try:
        df["date"] = pd.to_datetime(df["timestamp"]).dt.date
        df["thought_len"] = df["thought"].apply(lambda x: len(str(x)))
        df["response_len"] = df["response"].apply(lambda x: len(str(x)))
        df["alignment"] = 1.0 - (
            abs(df["thought_len"] - df["response_len"]) /
            df[["thought_len", "response_len"]].max(axis=1).replace(0, 1)
        )
        df["alignment"] = df["alignment"].clip(0.0, 1.0).round(3)
        trend_df = df.groupby("date")["alignment"].mean().reset_index()

        fig, ax = plt.subplots()
        ax.plot(trend_df["date"], trend_df["alignment"], marker='o', linestyle='-')
        ax.set_title("Daily RCA Alignment Score")
        ax.set_xlabel("Date")
        ax.set_ylabel("Avg RCA Score")
        ax.grid(True)
        st.pyplot(fig)
    except Exception as e:
        st.warning(f"⚠️ RCA graph error: {e}")
else:
    st.info("Not enough data to plot RCA trend.")

# Thought Timeline
st.markdown("---")
st.subheader("🧠 Thought Timeline")
if filtered_memory:
    for entry in reversed(filtered_memory[-30:]):
        st.markdown(f"**{entry['timestamp']}**")
        if entry.get("tag"):
            st.markdown(f"🏷️ *{entry['tag']}*")
        st.code(f"🗯️ {entry['thought']}")
        st.success(f"🔁 {entry['response']}")
        st.markdown("---")
else:
    st.warning("No entries matched the current filter.")

