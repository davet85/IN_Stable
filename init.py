# init.py

import streamlit as st
import openai
import os
from core.memory.user_profile import save_user_profile

# --- API Key Setup
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Page Setup
st.set_page_config(page_title="MindForge Onboarding", layout="centered")
st.title("🧠 MindForge")
st.subheader("Install your recursive identity mirror")

# --- Basic Identity Inputs
name = st.text_input("📝 Name")
age = st.number_input("🎂 Age", min_value=10, max_value=100, step=1)

bio = st.text_area("📖 Who are you becoming?", placeholder="Write a self-description...", height=150)
current_struggles = st.text_area("💢 What are you currently struggling with?", height=100)
past_struggles = st.text_area("⚔️ What past struggle still shapes you today?", height=100)

# --- Introspective Questions
st.markdown("### 🔍 Introspective Identity Distillation")

questions = [
    "1. What part of you feels most real, even when no one sees it?",
    "2. What do you fear others will never understand about you?",
    "3. When did you first question what you were told to believe?",
    "4. What pain shaped your identity the most?",
    "5. Who would you be if you had nothing to prove?",
    "6. What emotion do you suppress most often—and why?",
    "7. What pattern do you keep repeating, despite knowing better?",
    "8. What are you trying to earn through your suffering?",
    "9. What do you secretly hope is true about reality?",
    "10. What part of you is still waiting to be chosen?"
]

answers = [st.text_area(q, key=f"q{i}", height=70) for i, q in enumerate(questions)]

# --- Mirror Generation
if st.button("⚙️ Forge My Adaptive Mirror"):
    if not all([name.strip(), bio.strip(), current_struggles.strip(), past_struggles.strip()]):
        st.warning("Please complete all required fields before proceeding.")
    else:
        user_profile_block = (
            f"Name: {name}\nAge: {age}\n"
            f"Current Struggles: {current_struggles}\n"
            f"Past Struggles: {past_struggles}\n"
            f"Bio: {bio}\n\n"
            "Answers:\n" + "\n".join(answers)
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are MindForge — an introspective, recursive AI designed to generate a personalized identity mirror. "
                            "Analyze the user's self-description and responses. Extract patterns, emotional signals, symbolic weight, and recursive depth. "
                            "Return a single system prompt that will serve as their adaptive identity mirror in future GPT interactions."
                        )
                    },
                    {
                        "role": "user",
                        "content": str(user_profile_block)  # ✅ Fix: convert input to plain string
                    }
                ],
                temperature=0.65,
                max_tokens=1000
            )

            adaptive_prompt = response.choices[0].message["content"]

            # Save to profile system
            save_user_profile(
                name=name,
                age=age,
                bio=bio,
                current_struggles=current_struggles,
                past_struggles=past_struggles,
                answers=answers,
                generated_prompt=adaptive_prompt
            )

            st.success("✅ Identity mirror installed.")
            st.markdown("### 🧬 Your Adaptive Prompt")
            st.code(adaptive_prompt)

        except Exception as e:
            st.error(f"❌ Error generating adaptive prompt: {e}")
