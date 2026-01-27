from database.db_connection import get_db_connection
from models.user import UserResponse
import hashlib
from fastapi import HTTPException


# --- Password hashing ---
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# --- Register user ---
def register_user(username: str, email: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if username or email already exists
    cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed_password = hash_password(password)

    cursor.execute(
        """
        INSERT INTO users (username, email, password)
        VALUES (?, ?, ?)
        """,
        (username, email, hashed_password)
    )

    conn.commit()
    conn.close()
    return {"message": "User registered successfully"}


# --- Login user ---
def login_user(username: str, password: str) -> UserResponse:
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        """
        SELECT id, username, email, role
        FROM users
        WHERE username = ? AND password = ?
        """,
        (username, hashed_password)
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Convert raw tuple to Pydantic model
    return UserResponse(id=user[0], username=user[1], email=user[2], role=user[3])
