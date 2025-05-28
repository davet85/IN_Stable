# gpt/gpt_handler.py

import os
from openai import OpenAI

# Get API key from environment
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found. Set it in your .env or Streamlit Cloud Secrets.")

# Instantiate OpenAI client
client = OpenAI(api_key=api_key)

def handle_prompt(prompt: str) -> str:
    """Send user prompt to OpenAI and return response."""
    if not prompt.strip():
        return "⚠️ No input provided."

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful cognitive reflection assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ API Error: {str(e)}"
