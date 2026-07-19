import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

# FIXED: Explicitly target the 'backend' folder where your .env is located
base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / ".env"
load_dotenv(dotenv_path=env_path)

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "customer_support_db")

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def connect_to_mongo():
    if not MONGODB_URL:
        raise ValueError(f"MONGODB_URL environment variable is missing! Looked at: {env_path}")
        
    try:
        db_instance.client = AsyncIOMotorClient(MONGODB_URL)
        db_instance.db = db_instance.client[DATABASE_NAME]
        
        # Force a connection check
        await db_instance.client.admin.command('ping')
        print("\n========================================================")
        print("✅ SUCCESS: MongoDB Atlas is connected securely!")
        print("========================================================\n")
    except Exception as e:
        print("\n========================================================")
        print("❌ DATABASE CONNECTION FAILED ON STARTUP!")
        print(f"Error Details: {e}")
        print("========================================================\n")
        raise e

async def close_mongo_connection():
    if db_instance.client:
        db_instance.client.close()
        print("MongoDB Atlas connection closed.")

def get_database():
    return db_instance.db