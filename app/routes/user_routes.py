from fastapi import APIRouter, Depends, HTTPException, Request

from app.crud.user_crud import fetch_user_details
from app.models.user_model import UserPublic
from app.utils.depends import require_authenticated_user
from database import get_users_collection
from motor.motor_asyncio import AsyncIOMotorCollection

router = APIRouter()

@router.get("/user_details/{user_id}", response_model=UserPublic)
async def get_user_details(
    user_id: str,
    users_collection: AsyncIOMotorCollection = Depends(get_users_collection),
    user=Depends(require_authenticated_user)
):
    try:
        user_doc = await fetch_user_details(user_id, users_collection)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    user_doc["_id"] = str(user_doc["_id"])
    return UserPublic(**user_doc)
