import sqlite3
from pathlib import Path

# Absolute path to finance.db
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "finance.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
