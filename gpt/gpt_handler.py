# gpt/gpt_handler.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file for API keys

# Get API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("⚠️ OPENAI_API_KEY not found in environment.")

openai.api_key = OPENAI_API_KEY

def handle_prompt(prompt: str) -> str:
    """Sends a user prompt to OpenAI and returns the assistant's response."""
    if not prompt.strip():
        return "⚠️ No input provided."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Or switch to "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful cognitive reflection assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except openai.error.AuthenticationError:
        return "❌ API authentication f
