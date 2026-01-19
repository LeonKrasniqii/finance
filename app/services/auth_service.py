import hashlib
import sqlite3
from datetime import datetime

from database.db_connection import get_db_connection
from models.user import User


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def register_user(username: str, password: str):
    password_hash = hash_password(password)
    created_at = datetime.utcnow().isoformat()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (username, password_hash, created_at)
            VALUES (?, ?, ?)
        """, (username, password_hash, created_at))

        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id

    except sqlite3.IntegrityError:
        conn.close()
        return None


def login_user(username: str, password: str):
    password_hash = hash_password(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, created_at
        FROM users
        WHERE username = ? AND password_hash = ?
    """, (username, password_hash))

    row = cursor.fetchone()
    conn.close()

    if row:
        return User(
            id=row[0],
            username=row[1],
            created_at=row[2]
        )

    return None
