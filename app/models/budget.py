from app.database.db_connection import get_db_connection


def create_budget(user_id, category_id, month, year, monthly_limit):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO budget (user_id, category_id, month, year, monthly_limit)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, category_id, month, year, monthly_limit))

    conn.commit()
    conn.close()


def get_budgets_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            b.id,
            b.month,
            b.year,
            b.monthly_limit,
            c.name AS category_name
        FROM budget b
        JOIN categories c ON b.category_id = c.id
        WHERE b.user_id = ?
        ORDER BY b.year DESC, b.month DESC
    """, (user_id,))

    budgets = cursor.fetchall()
    conn.close()
    return budgets


def get_budget_for_category(user_id, category_id, month, year):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, monthly_limit
        FROM budget
        WHERE user_id = ?
          AND category_id = ?
          AND month = ?
          AND year = ?
    """, (user_id, category_id, month, year))

    budget = cursor.fetchone()
    conn.close()
    return budget


def delete_budget(budget_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM budget
        WHERE id = ? AND user_id = ?
    """, (budget_id, user_id))

    conn.commit()
    conn.close()
