import bcrypt
import sqlite3
from app.database.db_connection import get_db_connection

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_user_by_username(username: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email, password, role FROM users WHERE username = ?", 
            (username,)
        )
        return cursor.fetchone()

def create_user(username, email, password, role="user"):
    hashed = hash_password(password)
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                (username, email, hashed, role)
            )
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None