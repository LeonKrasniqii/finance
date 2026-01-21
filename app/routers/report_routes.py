# app/routers/report_routes.py

from fastapi import APIRouter
from app.services.expense_service import get_user_expenses
from app.services.analysis_service import expense_summary

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/expenses/{user_id}")
def expense_report(user_id: int):
    expenses = get_user_expenses(user_id)
    summary = expense_summary(expenses)
    return summary
