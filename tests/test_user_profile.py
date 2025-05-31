# tests/test_user_profile.py

import sys
import json
from pathlib import Path

# ✅ Fix import path to project root (/IN_STABLE)
sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.memory.user_profile import save_user_profile

# --- Test Data
test_name = "Test User"
test_age = 42
test_bio = "Symbolic test case for identity storage verification."
test_current = "Struggling with recursion fatigue."
test_past = "Historically struggled with indecision and self-doubt."
test_answers = [f"Test answer {i+1}" for i in range(10)]
test_prompt = "You are a reflective mirror for testing purposes only."

# --- Save profile
save_user_profile(
    name=test_name,
    age=test_age,
    bio=test_bio,
    current_struggles=test_current,
    past_struggles=test_past,
    answers=test_answers,
    generated_prompt=test_prompt
)

# --- Verify output file
profile_path = Path("database/user_profile.json")
assert profile_path.exists(), "❌ Profile file not created."

with profile_path.open("r") as f:
    profile = json.load(f)

# --- Assertions
assert profile["name"] == test_name, "❌ Name mismatch"
assert profile["age"] == test_age, "❌ Age mismatch"
assert profile["bio"] == test_bio, "❌ Bio mismatch"
assert profile["current_struggles"] == test_current, "❌ Current struggles mismatch"
assert profile["past_struggles"] == test_past, "❌ Past struggles mismatch"
assert profile["answers"] == test_answers, "❌ Answers mismatch"
assert profile["active_prompt"] == test_prompt, "❌ Prompt mismatch"

print("✅ MindForge: Profile saved and verified successfully.")
