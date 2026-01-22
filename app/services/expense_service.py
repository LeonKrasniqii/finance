from app.database.db_connection import get_db_connection
from app.models.expense import ExpenseCreate, ExpenseResponse
from fastapi import HTTPException
from typing import List


# --- Add a new expense ---
def add_expense(expense: ExpenseCreate) -> int:
    """
    Inserts a new expense into the database.
    Returns the new expense ID.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO expenses (user_id, category_id, amount, description, date)
                VALUES (?, ?, ?, ?, ?)
                """,
                (expense.user_id, expense.category_id, expense.amount, expense.description, expense.date)
            )
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Get all expenses for a user ---
def get_user_expenses(user_id: int) -> List[ExpenseResponse]:
    """
    Returns all expenses for a given user as a list of ExpenseResponse models.
    """
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

        # Convert raw rows to Pydantic models
        return [
            ExpenseResponse(
                id=row[0],
                user_id=row[1],
                category_id=row[2],
                amount=row[3],
                description=row[4],
                date=row[5]
            )
            for row in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
