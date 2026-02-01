from fastapi import APIRouter, HTTPException
from typing import List
from app.services.expense_service import get_user_expenses 
from pydantic import BaseModel

router = APIRouter(prefix="/reports", tags=["Reports"])

class ExpenseDetailed(BaseModel):
    id: int
    user_id: int          # Added: To track which user owns the expense
    category_id: int      # Added: This is the PERMANENT ID for Swagger
    username: str
    category_name: str
    amount: float
    description: str
    date: str

@router.get("/expenses/{user_id}", response_model=List[ExpenseDetailed])
def read_expense_report(user_id: int):
    expenses = get_user_expenses(user_id)
    
    if not expenses:
        return []
    
    return expenses