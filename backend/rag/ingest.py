import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Define absolute paths to ensure the script finds your folders
base_dir = Path(__file__).resolve().parent.parent.parent
kb_dir = base_dir / "knowledge_base"
db_dir = base_dir / "backend" / "vectorstore" / "faiss_index"

def build_vector_database():
    print("1. Loading PDFs from knowledge_base folder...")
    if not os.path.exists(kb_dir) or not os.listdir(kb_dir):
        print(f"Error: No PDFs found in {kb_dir}")
        return

    loader = PyPDFDirectoryLoader(str(kb_dir))
    documents = loader.load()
    print(f"Loaded {len(documents)} document pages.")

    print("2. Splitting text into readable chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, 
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")

    print("3. Generating embeddings using all-MiniLM-L6-v2...")
    # This downloads the open-source embedding model to your machine
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("4. Storing embeddings in FAISS Vector Database...")
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    # Save the database locally so agents can read it later
    vector_store.save_local(str(db_dir))
    print(f"✅ Vector database successfully built and saved to {db_dir}!")

if __name__ == "__main__":
    build_vector_database()