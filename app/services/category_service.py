from app.database.db_connection import get_db_connection

def get_all_categories():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM categories")
        rows = cursor.fetchall()
        return [{"id": r[0], "name": r[1]} for r in rows]

def add_category(name: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        return cursor.lastrowid

def delete_category(category_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Enable PRAGMA because SQLite needs it per connection for CASCADE to work
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return False, "Category not found."
        return True, "Category and all linked data deleted via CASCADE."