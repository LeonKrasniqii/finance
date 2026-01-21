
import sqlite3
from contextlib import contextmanager
from app.config import DATABASE_URL


def create_connection():
    """
    Create and return a SQLite database connection.
    """
    try:
        conn = sqlite3.connect(
            DATABASE_URL,
            check_same_thread=False
        )
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise RuntimeError(f"Database connection failed: {e}")


@contextmanager
def get_db():
    """
    Context manager for database operations.
    Automatically commits or rolls back.
    """
    conn = create_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Database operation failed: {e}")
    finally:
        conn.close()
