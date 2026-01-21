# app/routers/auth_routes.py

from fastapi import APIRouter, HTTPException
from app.services.auth_service import create_user, authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(username: str, email: str, password: str):
    try:
        create_user(username, email, password)
        return {"message": "User registered successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="User already exists")


@router.post("/login")
def login(username: str, password: str):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user)
    return {"access_token": token, "token_type": "bearer"}
