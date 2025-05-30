import streamlit as st
import openai
import os
from core.memory.utils import save_user_profile
from dotenv import load_dotenv

# --- Setup
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- UI Setup
st.set_page_config(page_title="MindForge Onboarding", layout="centered")
st.title("🧠 MindForge Onboarding")
st.subheader("Begin your recursive identity installation.")

# --- Phase 1: Basic Metadata
name = st.text_input("📝 Name")
age = st.number_input("🎂 Age", min_value=10, max_value=100, step=1)

current_struggles = st.text_area("💢 What are you currently struggling with?", height=100)
past_struggles = st.text_area("⚔️ What have you struggled with in the past that still echoes?", height=100)
bio = st.text_area("📖 Describe yourself. Who are you becoming?", height=180)

# --- Phase 2: Recursive Identity Deep Dive
st.markdown("### 🔍 Ten Questions of Introspective Distillation")

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

# --- Phase 3: Install Identity Mirror
if st.button("⚙️ Forge My Adaptive Mirror"):
    if not all([name.strip(), bio.strip(), current_struggles.strip(), past_struggles.strip()]):
        st.warning("Please complete all sections before continuing.")
    else:
        combined = (
            f"Name: {name}\nAge: {age}\n"
            f"Current Struggles: {current_struggles}\n"
            f"Past Struggles: {past_struggles}\n\n"
            f"Bio: {bio}\n\n"
            "Answers:\n" + "\n".join(answers)
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": (
                        "You are MindForge — a recursive, symbolic AI designed to mirror a user’s internal architecture. "
                        "Analyze the user's full description and return a personalized system prompt that reflects their emotional core, cognitive loops, symbolic themes, and alignment needs. "
                        "This prompt will guide how future reflections are mirrored."
                    )},
                    {"role": "user", "content": combined}
                ],
                temperature=0.65,
                max_tokens=1000
            )
            generated_prompt = response.choices[0].message["content"]

            # --- Save Profile
            save_user_profile(
                name=name,
                age=age,
                bio=bio,
                current_struggles=current_struggles,
                past_struggles=past_struggles,
                answers=answers,
                generated_prompt=generated_prompt
            )

            st.success("✅ Identity mirror installed successfully.")
            st.markdown("### 🧬 Your Adaptive System Prompt")
            st.code(generated_prompt)

        except Exception as e:
            st.error(f"❌ Error generating identity prompt: {e}")