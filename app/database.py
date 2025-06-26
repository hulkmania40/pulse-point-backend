from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

MONGO_URL = os.getenv("MONGODB_URI")
MONGO_DB_NAME = os.getenv("DB_NAME")

client = AsyncIOMotorClient(MONGO_URL, tlsCAFile=certifi.where())
db = client[MONGO_DB_NAME]
