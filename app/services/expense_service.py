from app.database.db_connection import get_db_connection

def get_user_expenses(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # FIXED: Added e.user_id and c.id (as category_id) to the SELECT
        query = """
            SELECT 
                e.id, 
                e.user_id,
                c.id as category_id,
                u.username, 
                c.name as category_name, 
                e.amount, 
                e.description, 
                e.date 
            FROM expenses e
            JOIN users u ON e.user_id = u.id
            JOIN categories c ON e.category_id = c.id
            WHERE e.user_id = ?
        """
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        
        # FIXED: Updated dictionary mapping to include the new columns
        return [
            {
                "id": r[0], 
                "user_id": r[1],
                "category_id": r[2], # This is the static ID for Swagger
                "username": r[3], 
                "category_name": r[4], 
                "amount": r[5], 
                "description": r[6], 
                "date": r[7]
            } for r in rows
        ]

def delete_expense(expense_id: int, user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (expense_id, user_id))
        conn.commit()
        return cursor.rowcount > 0

def add_expense(user_id: int, expense_data):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (user_id, category_id, amount, description, date) VALUES (?, ?, ?, ?, ?)",
            (user_id, expense_data.category_id, expense_data.amount, expense_data.description, expense_data.date)
        )
        conn.commit()
        return cursor.lastrowid