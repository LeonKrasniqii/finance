from fastapi import APIRouter, HTTPException
from typing import Dict, List
from app.routers.admin_routes import decode_token
from app.services.expense_service import get_user_expenses
from app.services.analysis_service import expense_summary
from app.models.expense import ExpenseResponse
from pydantic import BaseModel

router = APIRouter(prefix="/reports", tags=["Reports"])


# --- Pydantic model for expense summary ---
class ExpenseSummaryResponse(BaseModel):
    total_amount: float
    category_breakdown: Dict[str, float]


# --- READ: expense report for a user ---
@router.get("/expenses/{user_id}", response_model=ExpenseSummaryResponse)
def read_expense_report(user_id: int):
    expenses: List[ExpenseResponse] = get_user_expenses(user_id)

    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found for this user")

    summary = expense_summary(expenses)
    return ExpenseSummaryResponse(**summary)


# --- READ: expense report by category ---
@router.get("/expenses/{user_id}/category/{category}", response_model=ExpenseSummaryResponse)
def read_expense_report_by_category(user_id: int, category: str):
    expenses: List[ExpenseResponse] = get_user_expenses(user_id)

    filtered = [e for e in expenses if e.category_name == category]
    if not filtered:
        raise HTTPException(status_code=404, detail="No expenses found for this category")

    summary = expense_summary(filtered)
    return ExpenseSummaryResponse(**summary)


# --- CREATE: generate & return report (same as read but explicit) ---
@router.post("/expenses/{user_id}", response_model=ExpenseSummaryResponse)
def create_expense_report(user_id: int):
    expenses: List[ExpenseResponse] = get_user_expenses(user_id)

    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found for this user")

    summary = expense_summary(expenses)
    return ExpenseSummaryResponse(**summary)


# --- DELETE: clear report cache (future-proof) ---
@router.delete("/expenses/{user_id}")
def delete_expense_report(user_id: int):
    """
    Placeholder: if you later cache reports in Redis/DB
    """
    return {"message": f"Report cache cleared for user {user_id}"}
