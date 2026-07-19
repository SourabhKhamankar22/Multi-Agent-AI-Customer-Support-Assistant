import os
from google import genai
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / ".env"
load_dotenv(dotenv_path=env_path)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def handle_technical_query(user_query: str) -> str:
    """
    Generates a response for technical support issues (login, bugs, installation).
    """
    prompt = f"""
    You are the Technical Support Agent for a software company. 
    A customer has reached out with the following technical issue:
    
    "{user_query}"
    
    Your goal is to provide a polite, clear, and actionable troubleshooting step. 
    If the issue is missing details (like an error code), ask for them. 
    Keep the response professional, concise, and empathetic.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite', # OR 'gemini-3.5-flash'
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"I apologize, but I am having trouble connecting to our technical systems right now. Error: {e}"

# Local testing
if __name__ == "__main__":
    test_query = "How do I reset my password?"
    print(f"Customer: {test_query}")
    print(f"Technical Agent: {handle_technical_query(test_query)}")