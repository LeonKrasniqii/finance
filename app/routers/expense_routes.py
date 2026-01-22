from fastapi import APIRouter, HTTPException
from app.services.expense_service import add_expense, get_user_expenses
from app.models.expense import ExpenseCreate, ExpenseResponse
from typing import List

router = APIRouter(prefix="/expenses", tags=["Expenses"])


# --- Create a new expense ---
@router.post("/", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate):
    """
    Add a new expense
    """
    try:
        expense_id = add_expense(
            user_id=expense.user_id,
            category_id=expense.category_id,
            amount=expense.amount,
            description=expense.description,
            date=expense.date
        )
        # Return full ExpenseResponse
        return ExpenseResponse(id=expense_id, **expense.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- List expenses for a user ---
@router.get("/{user_id}", response_model=List[ExpenseResponse])
def list_expenses(user_id: int):
    expenses = get_user_expenses(user_id)
    # Expenses should already be Pydantic models
    return expenses
