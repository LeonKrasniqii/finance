# app/services/auth_service.py

import hashlib
import jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.database.db_connection import get_db
from app.models.user import User


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(username: str, email: str, password: str):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hash_password(password))
        )


def authenticate_user(username: str, password: str):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, hash_password(password))
        )
        row = cursor.fetchone()
        if not row:
            return None
        return User(row["id"], row["username"], row["email"], row["role"])


def create_access_token(user: User):
    payload = {
        "sub": user.username,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
