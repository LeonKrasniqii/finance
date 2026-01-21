# app/routers/admin_routes.py

from fastapi import APIRouter, HTTPException
from app.database.db_connection import get_db
from app.services.auth_service import decode_token

router = APIRouter(prefix="/admin", tags=["Admin"])


def admin_required(token: str):
    """
    Simple role-based authorization check
    """
    payload = decode_token(token)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload


@router.get("/users")
def get_all_users(token: str):
    admin_required(token)

    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT id, username, email, role FROM users")
        users = cursor.fetchall()

    return [dict(u) for u in users]


@router.get("/expenses")
def get_all_expenses(token: str):
    admin_required(token)

    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT expenses.id, users.username, categories.name AS category,
                   expenses.amount, expenses.description, expenses.date
            FROM expenses
            JOIN users ON expenses.user_id = users.id
            JOIN categories ON expenses.category_id = categories.id
        """)
        expenses = cursor.fetchall()

    return [dict(e) for e in expenses]


@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, token: str):
    admin_required(token)

    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Expense not found")

    return {"message": "Expense deleted successfully"}
