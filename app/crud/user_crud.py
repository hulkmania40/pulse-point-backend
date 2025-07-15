from motor.motor_asyncio import AsyncIOMotorCollection
from passlib.context import CryptContext
from bson import ObjectId
from datetime import datetime

from app.models.user_model import UserCreate, UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔐 Password utils
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ✅ Create user
async def create_user(user_data: UserCreate, users_collection: AsyncIOMotorCollection):
    existing = await users_collection.find_one({"username": user_data.username})
    if existing:
        raise ValueError("Username already exists")

    if user_data.email:
        email_exists = await users_collection.find_one({"email": user_data.email})
        if email_exists:
            raise ValueError("Email already in use")

    if user_data.mobile:
        mobile_exists = await users_collection.find_one({"mobile": user_data.mobile})
        if mobile_exists:
            raise ValueError("Mobile already in use")

    now = datetime.utcnow()
    user = UserInDB(
        **user_data.dict(exclude={"password", "created_at", "updated_at"}),
        hashed_password=hash_password(user_data.password),
        created_at=now,
        updated_at=now
    )

    result = await users_collection.insert_one(user.dict(by_alias=True))
    return str(result.inserted_id)

# ✅ Get user by username or email
async def get_user_by_identifier(identifier: str, users_collection: AsyncIOMotorCollection):
    user = await users_collection.find_one({
        "$or": [{"username": identifier}, {"email": identifier}]
    })
    return user

# ✅ Verify user credentials and return user if valid
async def verify_user(identifier: str, password: str, users_collection: AsyncIOMotorCollection):
    user = await get_user_by_identifier(identifier, users_collection)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

async def fetch_user_details(user_id: str, users_collection: AsyncIOMotorCollection):
    try:
        return await users_collection.find_one({ "_id": ObjectId(user_id) })
    except Exception:
        return None  # in case of invalid ObjectId format