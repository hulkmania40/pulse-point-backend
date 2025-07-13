from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from bson import ObjectId
from datetime import datetime

# 👇 Helper to handle ObjectId in Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")

# ✅ Base User model (shared fields)
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: Optional[EmailStr] = None
    mobile: Optional[str] = Field(None, pattern=r"^\d{10}$")
    role: str = "viewer"
    email_verified: bool = False
    mobile_verified: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# ✅ Model used for creating a user (input)
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

# ✅ Model used for database response/output
class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# ✅ Model used for user login
class UserLogin(BaseModel):
    identifier: str  # can be username or email
    password: str

# ✅ Model used for returning user info to frontend (excluding password)
class UserPublic(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
