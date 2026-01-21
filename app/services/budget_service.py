# app/services/budget_service.py

from app.database.db_connection import get_db


def set_budget(user_id, category_id, monthly_limit):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO budgets (user_id, category_id, monthly_limit)
            VALUES (?, ?, ?)
            """,
            (user_id, category_id, monthly_limit)
        )


def get_budgets(user_id):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM budgets WHERE user_id=?", (user_id,)
        )
        return cursor.fetchall()
