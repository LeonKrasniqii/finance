from app.database.db_connection import get_db_connection


def create_categories(name, description=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO categories (name, description)
        VALUES (?, ?)
    """, (name, description))

    conn.commit()
    conn.close()


def get_all_categories():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, description
        FROM categories
        ORDER BY name
    """)

    categories = cursor.fetchall()
    conn.close()
    return categories


def get_categories_by_id(category_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, description
        FROM categories
        WHERE id = ?
    """, (category_id,))

    category = cursor.fetchone()
    conn.close()
    return category


def delete_categories(category_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM categories
        WHERE id = ?
    """, (category_id,))

    conn.commit()
    conn.close()
