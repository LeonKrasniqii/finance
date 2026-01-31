from fastapi import APIRouter, HTTPException, Header, status
from typing import Optional, List

from app.services.expense_service import add_expense, get_user_expenses, get_expense_by_id, update_expense, delete_expense
from app.models.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse

router = APIRouter(prefix="/expenses", tags=["Expenses"])

# --- CREATE ---
@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: ExpenseCreate,
    x_user_id: Optional[str] = Header(None)  # header is string
):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="User not provided")

    try:
        user_id = int(x_user_id)
        expense_id = add_expense(
            user_id=user_id,
            expense=expense
        )
        return ExpenseResponse(id=expense_id, user_id=user_id, **expense.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- READ (all by user) ---
@router.get("/me", response_model=List[ExpenseResponse])
def read_my_expenses(x_user_id: Optional[str] = Header(None)):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="User not provided")
    user_id = int(x_user_id)
    return get_user_expenses(user_id)

# --- READ (single expense) ---
@router.get("/{expense_id}", response_model=ExpenseResponse)
def read_expense(expense_id: int):
    expense = get_expense_by_id(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

# --- UPDATE ---
@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense_route(
    expense_id: int,
    expense: ExpenseUpdate,
    x_user_id: Optional[str] = Header(None)  # header required for security
):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="User not provided")
    user_id = int(x_user_id)

    updated = update_expense(expense_id, expense)
    if not updated:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated

# --- DELETE ---
@router.delete("/{expense_id}")
def delete_expense_route(expense_id: int):
    deleted = delete_expense(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted successfully"}
