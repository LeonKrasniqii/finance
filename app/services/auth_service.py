from app.database.db_connection import get_db_connection
from app.models.user import UserResponse
from fastapi import HTTPException
import hashlib

# --- Password hashing ---
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# --- Register a new user ---
def register_user(username: str, email: str, password: str):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Check if username or email already exists
            cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Username or email already exists")

            # Insert user
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, hash_password(password))
            )

            conn.commit()
            return {"message": "User registered successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Login user ---
def login_user(username: str, password: str) -> UserResponse:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, email, role FROM users WHERE username = ? AND password = ?",
                (username, hash_password(password))
            )
            user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Return Pydantic model
        return UserResponse(id=user[0], username=user[1], email=user[2], role=user[3])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
