from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

MONGO_URL = os.getenv("MONGODB_URI")
MONGO_DB_NAME = os.getenv("DB_NAME")

client = AsyncIOMotorClient(MONGO_URL, tlsCAFile=certifi.where())
db = client[MONGO_DB_NAME]

# ✅ Dependency function to return the "users" collection
def get_users_collection() -> AsyncIOMotorCollection:
    return db["users"]