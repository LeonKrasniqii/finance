# app/routers/expense_routes.py

from fastapi import APIRouter
from app.services.expense_service import add_expense, get_user_expenses

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/")
def create_expense(user_id: int, category_id: int, amount: float, description: str, date: str):
    add_expense(user_id, category_id, amount, description, date)
    return {"message": "Expense added"}


@router.get("/{user_id}")
def list_expenses(user_id: int):
    expenses = get_user_expenses(user_id)
    return [e.to_dict() for e in expenses]
