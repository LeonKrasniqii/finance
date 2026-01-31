# app/services/expense_service.py
from app.models.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from app.database.db_connection import get_db_connection
from fastapi import HTTPException
from typing import List, Optional

# --- CREATE ---
def add_expense(user_id: int, expense: ExpenseCreate) -> int:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO expenses (user_id, category_id, amount, description, date) VALUES (?, ?, ?, ?, ?)",
                (user_id, expense.category_id, expense.amount, expense.description, expense.date),
            )
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- READ all by user ---
def get_user_expenses(user_id: int) -> List[ExpenseResponse]:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, user_id, category_id, amount, description, date FROM expenses WHERE user_id=?",
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
                    date=row[5]
                )
                for row in rows
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- READ single expense ---
def get_expense_by_id(expense_id: int) -> Optional[ExpenseResponse]:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, user_id, category_id, amount, description, date FROM expenses WHERE id=?",
                (expense_id,)
            )
            row = cursor.fetchone()
            if row:
                return ExpenseResponse(
                    id=row[0],
                    user_id=row[1],
                    category_id=row[2],
                    amount=row[3],
                    description=row[4],
                    date=row[5]
                )
            return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- UPDATE ---
def update_expense(expense_id: int, expense: ExpenseUpdate) -> Optional[ExpenseResponse]:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE expenses SET category_id=?, amount=?, description=?, date=? WHERE id=?",
                (expense.category_id, expense.amount, expense.description, expense.date, expense_id)
            )
            conn.commit()
            return get_expense_by_id(expense_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- DELETE ---
def delete_expense(expense_id: int) -> bool:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
