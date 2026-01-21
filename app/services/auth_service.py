from app.database.db_connection import get_db_connection
import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username: str, email: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (username, email, password)
        VALUES (?, ?, ?)
        """,
        (username, email, hash_password(password))
    )

    conn.commit()
    conn.close()


def login_user(username: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username, email, role
        FROM users
        WHERE username = ? AND password = ?
        """,
        (username, hash_password(password))
    )

    user = cursor.fetchone()
    conn.close()
    return user
