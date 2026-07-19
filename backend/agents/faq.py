import os
from google import genai
from dotenv import load_dotenv
from pathlib import Path

# 1. IMPORT THE RAG RETRIEVER
from backend.rag.retriever import get_relevant_context

base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / ".env"
load_dotenv(dotenv_path=env_path)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def handle_faq_query(user_query: str) -> str:
    """Generates a RAG-augmented response for general questions."""
    
    # 2. SEARCH THE VECTOR DATABASE
    company_context = get_relevant_context(user_query)
    
    prompt = f"""
    You are the General FAQ Agent for TechMart Electronics. 
    A customer has asked the following question:
    "{user_query}"
    
    Answer their question accurately using ONLY the official company information provided below. 
    If the answer is not in the text, politely say you do not know. Do not guess locations or policies.
    
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
        return f"I apologize, but I cannot access our knowledge base right now. Error: {e}"