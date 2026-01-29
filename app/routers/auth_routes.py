from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import bcrypt
import jwt

from app.database.db_connection import get_db_connection
from app.models.user import UserResponse

# --- JWT config ---
SECRET_KEY = "whfjhwjlhfdkahfl"  # Change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(tags=["Auth"])

# --- Request models ---
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# --- Password helpers ---
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

# --- JWT helpers ---
def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# --- Register route ---
@router.post("/register")
def register(data: RegisterRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (data.username, data.email))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed_password = hash_password(data.password)
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (data.username, data.email, hashed_password)
    )
    conn.commit()
    conn.close()
    return {"message": "User registered successfully"}

# --- Login route ---
@router.post("/login")
def login(data: LoginRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, email, role, password FROM users WHERE username = ?",
        (data.username,)
    )
    user = cursor.fetchone()
    conn.close()

    if not user or not verify_password(data.password, user[4]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Create JWT token
    token_data = {"user_id": user[0], "username": user[1], "role": user[3]}
    access_token = create_access_token(token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(id=user[0], username=user[1], email=user[2], role=user[3])
    }
