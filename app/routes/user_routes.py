from fastapi import APIRouter, Depends, Request

from app.crud.user_crud import fetch_user_details
from app.models.user_model import UserPublic
from app.utils.depends import require_authenticated_user
from database import get_users_collection
from motor.motor_asyncio import AsyncIOMotorCollection

router = APIRouter()

@router.get("/user_details/{user_id}", response_model=UserPublic)
async def get_user_detials(user_id: str,users_collection: AsyncIOMotorCollection = Depends(get_users_collection),user=Depends(require_authenticated_user)):
    return await fetch_user_details(user_id, users_collection)