from fastapi import APIRouter, HTTPException, status
from typing import List
from app.database.db_connection import get_db_connection
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["Admin"])

# Pydantic 
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

class ExpenseResponse(BaseModel):
    id: int
    user_id: int
    title: str
    amount: float
    category: str
    date: datetime



# USER MANAGEMENT

@router.get("/users", response_model=List[UserResponse])
def get_all_users():
    """
    Get a list of all users in the system.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, role, created_at FROM users")
    users = cursor.fetchall()
    conn.close()

    return [dict(user) for user in users]


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """
    Delete a user by ID. Be careful!
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    return



# EXPENSE MANAGEMENT

@router.get("/expenses", response_model=List[ExpenseResponse])
def get_all_expenses():
    """
    Get all expenses across all users.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = cursor.fetchall()
    conn.close()

    return [dict(expense) for expense in expenses]


@router.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int):
    """
    Delete any expense by ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

    return



# ADMIN REPORTS

@router.get("/reports/total")
def get_system_total_expenses():
    """
    Get total expenses across all users.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) as total FROM expenses")
    result = cursor.fetchone()
    conn.close()

    total = result["total"] if result["total"] is not None else 0
    return {"total_expenses": total}


@router.get("/reports/category")
def get_system_expenses_by_category():
    """
    Get total expenses grouped by category across all users.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        GROUP BY category
    """)
    result = cursor.fetchall()
    conn.close()

    return {"category_totals": [dict(row) for row in result]}
