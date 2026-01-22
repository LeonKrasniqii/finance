from fastapi import APIRouter, HTTPException
from app.services.expense_service import get_user_expenses
from app.services.analysis_service import expense_summary
from app.models.expense import ExpenseResponse
from pydantic import BaseModel
from typing import Dict, List

router = APIRouter(prefix="/reports", tags=["Reports"])


# --- Pydantic model for expense summary ---
class ExpenseSummaryResponse(BaseModel):
    total_amount: float
    category_breakdown: Dict[str, float]


# --- Endpoint: expense report for a user ---
@router.get("/expenses/{user_id}", response_model=ExpenseSummaryResponse)
def expense_report(user_id: int):
    try:
        # Fetch user expenses (should return list of ExpenseResponse)
        expenses: List[ExpenseResponse] = get_user_expenses(user_id)
        
        if not expenses:
            raise HTTPException(status_code=404, detail="No expenses found for this user")
        
        # Generate summary
        summary = expense_summary(expenses)
        
        return ExpenseSummaryResponse(**summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
