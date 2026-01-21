from app.database.db_connection import get_db_connection


def add_expense(user_id, category_id, amount, description, date):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO expenses (user_id, category_id, amount, description, date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, category_id, amount, description, date)
    )

    conn.commit()
    conn.close()


def get_expenses_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            e.id,
            c.name AS category,
            e.amount,
            e.description,
            e.date
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        WHERE e.user_id = ?
        ORDER BY e.date DESC
        """,
        (user_id,)
    )

    expenses = cursor.fetchall()
    conn.close()
    return expenses
