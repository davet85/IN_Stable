# gpt/gpt_handler.py

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Instantiate client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
