from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel # FIXED
import jwt
from datetime import datetime, timedelta
from app.services.auth_service import get_user_by_username, verify_password, create_user

SECRET_KEY = "whfjhwjlhfdkahfl" 
ALGORITHM = "HS256"

router = APIRouter(tags=["Auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

def decode_access_token(token: str):
    try:
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        return None

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=2)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register")
def register(data: RegisterRequest):
    user_id = create_user(data.username, data.email, data.password)
    if not user_id:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"message": "Success", "user_id": user_id}

@router.post("/login")
def login(data: LoginRequest):
    user = get_user_by_username(data.username)
    if not user or not verify_password(data.password, user[3]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_payload = {"user_id": user[0], "username": user[1], "role": user[4]}
    token = create_access_token(token_payload)
    
    return {
        "access_token": token, 
        "token_type": "bearer", 
        "user": {"id": user[0], "username": user[1], "role": user[4]}
    }