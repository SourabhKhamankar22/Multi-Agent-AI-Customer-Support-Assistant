import os
from google import genai
from dotenv import load_dotenv
from pathlib import Path

# Automatically targets the root .env file
base_dir = Path(__file__).resolve().parent.parent.parent
env_path = base_dir / ".env"
load_dotenv(dotenv_path=env_path)

# Shared single client instance
_client = None

def get_genai_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client