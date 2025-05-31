# core/memory/utils.py
import json
from pathlib import Path

def save_user_profile(name, age, bio, current_struggles, past_struggles, answers, generated_prompt):
    profile_data = {
        "name": name,
        "age": age,
        "bio": bio,
        "current_struggles": current_struggles,
        "past_struggles": past_struggles,
        "answers": answers,
        "generated_prompt": generated_prompt
    }
    path = Path("database/user_profile.json")
    with path.open("w") as f:
        json.dump(profile_data, f, indent=2)
