from app.database.db_connection import get_db_connection
import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username: str, email: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()

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


def login_user(username: str, password: str):
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
    return user
