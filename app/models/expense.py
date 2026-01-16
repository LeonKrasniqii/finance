from app.database.db_connection import get_db_connection

def create_expense(user_id, category_id, amount, expense_date, description=None, payment_method=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (user_id, category_id, amount, expense_date, description, payment_method)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, category_id, amount, expense_date, description, payment_method))

    conn.commit()
    conn.close()


def get_expenses_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.*, c.name AS category_name
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        WHERE e.user_id = ?
        ORDER BY e.expense_date DESC
    """, (user_id,))

    expenses = cursor.fetchall()
    conn.close()
    return expenses


def delete_expense(expense_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ? AND user_id = ?
    """, (expense_id, user_id))

    conn.commit()
    conn.close()
