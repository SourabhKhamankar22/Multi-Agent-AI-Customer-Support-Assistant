import os
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Define absolute paths
base_dir = Path(__file__).resolve().parent.parent.parent
db_dir = base_dir / "backend" / "vectorstore" / "faiss_index"

def get_relevant_context(query: str, k: int = 2) -> str:
    """Searches the vector database for the most relevant text chunks."""
    if not os.path.exists(db_dir):
        print("Vector database not found. Returning empty context.")
        return ""

    # 1. Initialize the exact same embedding model used for ingestion
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    try:
        # 2. Load the FAISS database (allow_dangerous_deserialization is required for local pickle files in LangChain)
        vector_store = FAISS.load_local(
            str(db_dir), 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        
        # 3. Perform a similarity search based on the user's query
        docs = vector_store.similarity_search(query, k=k)
        
        # 4. Combine the retrieved chunks into a single text block
        context = "\n\n".join([doc.page_content for doc in docs])
        return context
        
    except Exception as e:
        print(f"Error retrieving context: {e}")
        return ""