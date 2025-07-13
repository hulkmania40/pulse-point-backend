from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.utils.jwt_utils import ALGORITHM, SECRET_KEY, decode_access_token
from database import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ✅ Get current user from token
async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decode_access_token(token)

    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "user_id": payload["sub"],
        "username": payload["username"],
        "role": payload["role"]
    }

# ✅ Any logged-in user
async def require_authenticated_user(request: Request):
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = auth_header.replace("Bearer ", "")  # ✅ Define token

    # ✅ Check if token is blacklisted
    blacklisted = await db["blacklisted_tokens"].find_one({"token": token})
    if blacklisted:
        raise HTTPException(status_code=401, detail="Token has been revoked")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # or enrich with user details
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ✅ Only editor or admin
async def require_editor(user: dict = Depends(get_current_user)):
    if user["role"] not in ["editor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only editors and admins can access this route."
        )
    return user

# ✅ Only admin
async def require_admin(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this route."
        )
    return user
