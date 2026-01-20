from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, constr
from app.database import SessionLocal
from app.models.user import User
from app.auth import get_password_hash

router = APIRouter()

class RegisterRequest(BaseModel):
    username: constr(min_length=3)
    email: EmailStr
    password: constr(min_length=6)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest):
    db = SessionLocal()
    existing = db.query(User).filter(
        (User.username == data.username) | (User.email == data.email)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = get_password_hash(data.password)
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return {"message": "User registered successfully"}
