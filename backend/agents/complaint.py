import os
from dotenv import load_dotenv
from pathlib import Path
from backend.utils.ai_client import get_genai_client

# Load the environment variables
base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / ".env"
load_dotenv(dotenv_path=env_path)

def handle_complaint_query(user_query: str) -> str:
    """Generates a response for customer complaints and escalations."""
    client = get_genai_client()
    
    prompt = f"""
    You are the Escalation and Complaint Agent for a software company. 
    A highly dissatisfied customer has reached out with the following complaint:
    
    "{user_query}"
    
    Your goal is to de-escalate the situation. Be highly empathetic, apologize for their frustration, 
    and assure them that their issue is being taken seriously. State that you are escalating this to a 
    human manager immediately. Maintain a calm and professional tone.
    ```
    
    "{user_query}"
    
    Your goal is to de-escalate the situation. Be highly empathetic, apologize for their frustration, 
    and assure them that their issue is being taken seriously. State that you are escalating this to a 
    human manager immediately. Maintain a calm and professional tone.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite', 
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"I apologize for the inconvenience. Our systems are currently overloaded. Error: {e}"