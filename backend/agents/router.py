import os
import json
import time
from pydantic import BaseModel
from google.genai import types
from dotenv import load_dotenv
from pathlib import Path
from backend.utils.ai_client import get_genai_client

# Import all Specialized Agents
from backend.agents.technical import handle_technical_query
from backend.agents.billing import handle_billing_query
from backend.agents.faq import handle_faq_query
from backend.agents.complaint import handle_complaint_query
from backend.agents.product import handle_product_query

# Load the environment variables
base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / ".env"
load_dotenv(dotenv_path=env_path)

# Define the EXACT structure we want using Pydantic
class RouteResponse(BaseModel):
    agent: str

def detect_intent(user_query: str, retries=3) -> str:
    """
    Analyzes the user's message and routes it to the correct specialized agent.
    Includes automatic retries for 503 server errors.
    """
    client = get_genai_client()
    
    prompt = f"""
    You are the intelligent routing manager for a customer support system. 
    Analyze the following user query and assign it to exactly one of these specialized agents:
    - Billing Agent
    - Technical Agent
    - Product Agent
    - Complaint Agent
    - FAQ Agent
    
    User Query: "{user_query}"
    """
    
    for attempt in range(retries):
        try:
            # Use response_schema to enforce the Pydantic model
            response = client.models.generate_content(
                model='gemini-3.1-flash-lite',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=RouteResponse,
                    temperature=0.1 # Keep randomness low for routing
                )
            )
            
            result = json.loads(response.text)
            return result.get("agent", "FAQ Agent")
            
        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "429" in error_msg:
                print(f"API busy (Attempt {attempt + 1}/{retries}). Waiting 8 seconds...")
                time.sleep(8)
            else:
                print(f"Unexpected Error: {e}")
                return "FAQ Agent"
                
    return "FAQ Agent"

# Quick local test
if __name__ == "__main__":
    test_queries = [
        "I paid yesterday but Premium is still locked.",
        "How do I reset my password?",
        "Your software deleted all my files, I demand to speak to a manager!",
        "What is the difference between the Basic and Pro tier?",
        "Where is your company headquarters located?"
    ]
    
    print("==========================================")
    print("Testing Multi-Agent Router Pipeline...")
    print("==========================================\n")
    
    for query in test_queries:
        print(f"Customer Query: '{query}'")
        routed_to = detect_intent(query)
        print(f"-> Routed to: [{routed_to}]\n")
        
        # Route execution logic
        if routed_to == "Technical Agent":
            response = handle_technical_query(query)
        elif routed_to == "Billing Agent":
            response = handle_billing_query(query)
        elif routed_to == "Complaint Agent":
            response = handle_complaint_query(query)
        elif routed_to == "Product Agent":
            response = handle_product_query(query)
        elif routed_to == "FAQ Agent":
            response = handle_faq_query(query)
        else:
            response = "Error: Agent not recognized."
            
        print(f"AI Response:\n{response}\n")
        print("-" * 50)
            
        # Delay to respect API rate limits
        time.sleep(8)