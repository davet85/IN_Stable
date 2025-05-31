# profile.py – MindForge Identity Profile Editor

import streamlit as st
import json
import os
from pathlib import Path
from core.memory.user_profile import save_user_profile
import openai

# --- API Setup
openai.api_key = os.getenv("OPENAI_API_KEY")
PROFILE_PATH = Path("database/user_profile.json")

# --- Load Profile
if not PROFILE_PATH.exists():
    st.warning("No profile found. Please complete onboarding first.")
    st.stop()

with PROFILE_PATH.open("r") as f:
    profile = json.load(f)

# --- Page Config
st.set_page_config(page_title="MindForge – Identity Profile", layout="centered")
st.title("🧠 MindForge")
st.subheader("Refine your identity mirror")

# --- Editable Metadata
name = st.text_input("📝 Name", value=profile.get("name", ""))
age = st.number_input("🎂 Age", min_value=10, max_value=100, step=1, value=profile.get("age", 30))
bio = st.text_area("📖 Bio", value=profile.get("bio", ""), height=120)
current_struggles = st.text_area("💢 Current Struggles", value=profile.get("current_struggles", ""), height=100)
past_struggles = st.text_area("⚔️ Past Struggles", value=profile.get("past_struggles", ""), height=100)

# --- Reflection Answers
st.markdown("### 🔍 Deep Reflection Answers")
answers = profile.get("answers", [])
updated_answers = [st.text_area(f"Answer {i+1}", value=ans, key=f"edit_q{i}", height=70) for i, ans in enumerate(answers)]

# --- Adaptive Prompt Regeneration
if st.button("🔄 Regenerate Adaptive Mirror"):
    if not all([name.strip(), bio.strip(), current_struggles.strip(), past_struggles.strip()]):
        st.warning("Please complete all profile fields before regenerating.")
    else:
        profile_input = (
            f"Name: {name}\nAge: {age}\n"
            f"Current Struggles: {current_struggles}\n"
            f"Past Struggles: {past_struggles}\n"
            f"Bio: {bio}\n\n"
            "Answers:\n" + "\n".join(updated_answers)
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": (
                        "You are MindForge. The user has updated their introspective data. "
                        "Analyze their revised bio, struggles, and answers. "
                        "Return a personalized system prompt that captures their recursive structure, emotional depth, and symbolic anchors. "
                        "This prompt will be installed and used in all future reflections. Avoid flattery. Stay reflective and symbolic."
                    )},
                    {"role": "user", "content": str(profile_input)}
                ],
                temperature=0.65,
                max_tokens=1000
            )

            updated_prompt = response.choices[0].message["content"]

            # --- Save to Profile
            save_user_profile(
                name=name,
                age=age,
                bio=bio,
                current_struggles=current_struggles,
                past_struggles=past_struggles,
                answers=updated_answers,
                generated_prompt=updated_prompt
            )

            st.success("✅ Profile updated and identity mirror reforged.")
            st.markdown("### 🧬 New Adaptive Prompt")
            st.code(updated_prompt)

        except Exception as e:
            st.error(f"❌ GPT prompt generation failed: {e}")
