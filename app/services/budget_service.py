from app.database.db_connection import get_db_connection

def upsert_budget(user_id: int, category_id: int, limit: float):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # SQLite 'UPSERT' syntax
        query = """
            INSERT INTO budgets (user_id, category_id, monthly_limit)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, category_id) 
            DO UPDATE SET monthly_limit = excluded.monthly_limit
        """
        cursor.execute(query, (user_id, category_id, limit))
        conn.commit()
        return True

def get_user_budgets(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Fetch monthly_limit from DB, but return it as 'amount' for the UI
        cursor.execute("SELECT category_id, monthly_limit FROM budgets WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        return [{"category_id": r[0], "amount": r[1]} for r in rows]
    
def remove_budget(user_id: int, category_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM budgets WHERE user_id = ? AND category_id = ?", 
            (user_id, category_id)
        )
        conn.commit()
        return cursor.rowcount > 0