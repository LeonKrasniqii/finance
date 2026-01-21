from app.database.db_connection import get_db_connection
from app.models.category import Category


def get_all_categories():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM categories ORDER BY name")
    rows = cursor.fetchall()
    conn.close()

    return [Category(row["id"], row["name"]) for row in rows]


def add_category(name: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO categories (name) VALUES (?)",
        (name,)
    )

    conn.commit()
    conn.close()
