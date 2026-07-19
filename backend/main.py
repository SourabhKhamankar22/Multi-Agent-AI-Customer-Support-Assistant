from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from datetime import datetime

# --- 1. IMPORT DATABASE & AUTH ---
from backend.database.mongodb import connect_to_mongo, close_mongo_connection, get_database
from backend.api.auth import router as auth_router, get_current_user

# --- 2. IMPORT AI AGENTS ---
from backend.agents.router import detect_intent
from backend.agents.technical import handle_technical_query
from backend.agents.billing import handle_billing_query
from backend.agents.complaint import handle_complaint_query
from backend.agents.product import handle_product_query
from backend.agents.faq import handle_faq_query

# --- 3. DATABASE LIFESPAN ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

# --- 4. APP INITIALIZATION & MIDDLEWARE ---
app = FastAPI(
    title="Multi-Agent AI Customer Support Assistant API",
    lifespan=lifespan
)

# FIXED: You cannot use ["*"] with allow_credentials=True. 
# We explicitly allow your Next.js frontend ports here.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 5. ROUTES ---
app.include_router(auth_router, prefix="/api")

class ChatRequest(BaseModel):
    query: str
    session_id: str = "default_session" 

@app.post("/chat")
async def chat_endpoint(
    request: ChatRequest, 
    current_user=Depends(get_current_user), 
    db=Depends(get_database)
):
    agent_type = detect_intent(request.query)
    
    if agent_type == "Technical Agent":
        response = handle_technical_query(request.query)
    elif agent_type == "Billing Agent":
        response = handle_billing_query(request.query)
    elif agent_type == "Complaint Agent":
        response = handle_complaint_query(request.query)
    elif agent_type == "Product Agent":
        response = handle_product_query(request.query)
    elif agent_type == "FAQ Agent":
        response = handle_faq_query(request.query)
    else:
        response = "System Error: Routing failed."
        
    chat_record = {
        "user_email": current_user["email"],
        "session_id": request.session_id,  
        "user_message": request.query,
        "ai_response": response,
        "agent_used": agent_type,
        "timestamp": datetime.utcnow()
    }
    await db.conversations.insert_one(chat_record)
        
    return {
        "agent_used": agent_type,
        "response": response
    }

@app.get("/history")
async def get_chat_history(
    current_user=Depends(get_current_user), 
    db=Depends(get_database)
):
    cursor = db.conversations.find({"user_email": current_user["email"]}).sort("timestamp", 1)
    
    history = []
    async for document in cursor:
        history.append({
            "session_id": document.get("session_id", "Legacy Chat"), 
            "user_message": document["user_message"],
            "ai_response": document["ai_response"],
            "agent_used": document.get("agent_used", "System"),
            "timestamp": document["timestamp"].isoformat()
        })
        
    return {"history": history}

@app.get("/")
async def root():
    return {"status": "running"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)