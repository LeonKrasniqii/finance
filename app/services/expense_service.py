from app.database.db_connection import get_db_connection
from app.models.expense import ExpenseCreate, ExpenseResponse
from fastapi import HTTPException
from typing import List

# --- Add a new expense (used by Streamlit) ---
def add_expense_from_ui(user_id: int, category_id: int, amount: float, description: str, date: str) -> int:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO expenses (user_id, category_id, amount, description, date)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, category_id, amount, description, date)
            )
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Get all expenses for a user (used by dashboard) ---
def get_user_expenses(user_id: int) -> List[ExpenseResponse]:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, user_id, category_id, amount, description, date
                FROM expenses
                WHERE user_id = ?
                ORDER BY date DESC
                """,
                (user_id,)
            )
            rows = cursor.fetchall()

        return [
            ExpenseResponse(
                id=row[0],
                user_id=row[1],
                category_id=row[2],
                amount=row[3],
                description=row[4],
                date=row[5],
            )
            for row in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
