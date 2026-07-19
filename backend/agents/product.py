import os
from google import genai
from dotenv import load_dotenv
from pathlib import Path

# 1. IMPORT THE RAG RETRIEVER
from backend.rag.retriever import get_relevant_context

# Load the environment variables
base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / ".env"
load_dotenv(dotenv_path=env_path)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def handle_product_query(user_query: str) -> str:
    """Generates a RAG-augmented response for product features and pricing."""
    
    # 2. SEARCH THE VECTOR DATABASE
    company_context = get_relevant_context(user_query)
    
    # 3. INJECT THE PDF DATA INTO THE PROMPT
    prompt = f"""
    You are the Product Specialist Agent for TechMart Electronics. 
    A customer has asked the following question:
    "{user_query}"
    
    Answer their question accurately using ONLY the official company information provided below. 
    Do not invent or guess pricing or features.
    
    OFFICIAL COMPANY INFORMATION:
    {company_context}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite', 
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"I apologize, I am unable to pull up the product catalog right now. Error: {e}"