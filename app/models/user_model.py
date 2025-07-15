from typing import Optional
from bson import ObjectId
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.common import PyObjectId

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

    @field_validator("mobile")
    def validate_mobile(cls, v):
        if v is None:
            return v
        if not v.isdigit() or len(v) != 10:
            raise ValueError("Mobile must be a 10-digit number")
        return v

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
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
