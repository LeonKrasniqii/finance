from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.auth_service import register_user, login_user
from app.models.user import UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

# Request models
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# --- REGISTER ---
@router.post("/register")
def register(request: RegisterRequest):
    try:
        user = register_user(request.username, request.email, request.password)
        return {
            "message": "User registered successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- LOGIN ---
@router.post("/login")
def login(request: LoginRequest):
    try:
        user: UserResponse = login_user(request.username, request.password)
        # For now, token is optional or fake
        access_token = "fake-token-for-demo"

        return {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            },
            "access_token": access_token,
            "token_type": "bearer"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
