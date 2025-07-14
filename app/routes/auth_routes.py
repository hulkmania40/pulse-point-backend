from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.crud.user_crud import create_user, verify_user
from app.models.user_model import UserCreate, UserLogin
from app.utils.depends import require_authenticated_user
from database import get_users_collection
from app.utils.jwt_utils import create_access_token, get_token_expiry
from motor.motor_asyncio import AsyncIOMotorCollection
from database import db

router = APIRouter(prefix="/auth", tags=["Auth"])

# ✅ Signup Route
@router.post("/signup", status_code=201)
async def signup(
    user_data: UserCreate,
    users_collection: AsyncIOMotorCollection = Depends(get_users_collection)
):
    try:
        user_id = await create_user(user_data, users_collection)
        return JSONResponse(content={"message": "User created successfully", "user_id": user_id})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ Login Route
@router.post("/login")
async def login(
    login_data: UserLogin,
    users_collection: AsyncIOMotorCollection = Depends(get_users_collection)
):
    user = await verify_user(login_data.identifier, login_data.password, users_collection)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username/email or password")

    # Auto-upgrade viewer to editor if both verifications are done
    if (
        user["role"] == "viewer"
        and user.get("email_verified") is True
        and user.get("mobile_verified") is True
    ):
        user["role"] = "editor"
        await users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"role": "editor"}}
        )

    # Create JWT token
    token = create_access_token(
        data={
            "sub": str(user["_id"]),
            "username": user["username"],
            "role": user["role"]
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "username": user["username"],
            "role": user["role"]
        }
    }

@router.post("/logout")
async def logout(
    request: Request,
    user=Depends(require_authenticated_user)
):
    # ✅ Extract token from header
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Authorization token missing")

    token = auth_header.replace("Bearer ", "")  # ✅ Define token here

    # ✅ Extract expiry time from JWT
    try:
        expires_at = get_token_expiry(token)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid token")

    # ✅ Insert token into blacklist
    await db["blacklisted_tokens"].insert_one({
        "token": token,
        "expires_at": expires_at
    })

    return JSONResponse(
        content={"message": f"Goodbye {user['username']}, you’ve been logged out!"},
        status_code=200
    )
