from fastapi import APIRouter, HTTPException
from typing import List

from app.database.db_connection import get_db_connection
from app.models.user import UserResponse
from app.models.expense import ExpenseResponse

router = APIRouter(prefix="/admin", tags=["Admin"])

# --- Helper to check if user is admin ---
def is_admin(user_id: int) -> bool:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            return result is not None and result[0] == "admin"
    except:
        return False

# --- Routes ---

@router.get("/users", response_model=List[UserResponse])
def get_all_users(user_id: int):
    if not is_admin(user_id):
        raise HTTPException(status_code=403, detail="Admin access required")

    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute("SELECT id, username, email, role FROM users")
        users = cursor.fetchall()

    return [UserResponse(id=u[0], username=u[1], email=u[2], role=u[3]) for u in users]


@router.get("/expenses", response_model=List[ExpenseResponse])
def get_all_expenses(user_id: int):
    if not is_admin(user_id):
        raise HTTPException(status_code=403, detail="Admin access required")

    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT id, user_id, category_id, amount, description, date
            FROM expenses
        """)
        expenses = cursor.fetchall()

    return [
        ExpenseResponse(
            id=e[0],
            user_id=e[1],
            category_id=e[2],
            amount=e[3],
            description=e[4],
            date=e[5]
        ) for e in expenses
    ]


@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, user_id: int):
    if not is_admin(user_id):
        raise HTTPException(status_code=403, detail="Admin access required")

    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Expense not found")
        db.commit()

    return {"message": "Expense deleted successfully"}
