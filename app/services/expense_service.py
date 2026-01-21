# app/services/expense_service.py

from app.database.db_connection import get_db
from app.models.expense import Expense


def add_expense(user_id, category_id, amount, description, date):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO expenses (user_id, category_id, amount, description, date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, category_id, amount, description, date)
        )


def get_user_expenses(user_id):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM expenses WHERE user_id=?", (user_id,))
        rows = cursor.fetchall()
        return [
            Expense(
                r["id"],
                r["user_id"],
                r["category_id"],
                r["amount"],
                r["description"],
                r["date"]
            ) for r in rows
        ]
