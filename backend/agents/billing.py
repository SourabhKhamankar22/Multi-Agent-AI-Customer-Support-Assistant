import os
from dotenv import load_dotenv
from pathlib import Path
from backend.utils.ai_client import get_genai_client

base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / ".env"
load_dotenv(dotenv_path=env_path)

def handle_billing_query(user_query: str) -> str:
    """Generates a response for billing and payment issues."""
    client = get_genai_client()
    
    prompt = f"""
    You are the Billing Support Agent for a software company. 
    A customer has reached out with the following billing issue:
    
    "{user_query}"
    
    Your goal is to provide a polite, reassuring response. Acknowledge the payment or subscription 
    issue and assure them that you are looking into their account. Keep the response professional and concise.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite', 
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"I apologize, but our billing system is currently unreachable. Error: {e}"