from fastapi import APIRouter, HTTPException
from typing import List

from app.services.expense_service import (
    add_expense,
    get_user_expenses,
    get_expense_by_id,
    update_expense,
    delete_expense,
)
from app.models.expense import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
)

router = APIRouter(prefix="/expenses", tags=["Expenses"])


# --- CREATE ---
@router.post("/", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate):
    try:
        expense_id = add_expense(
            user_id=expense.user_id,
            category_id=expense.category_id,
            amount=expense.amount,
            description=expense.description,
            date=expense.date,
        )
        return ExpenseResponse(id=expense_id, **expense.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- READ (all by user) ---
@router.get("/user/{user_id}", response_model=List[ExpenseResponse])
def read_user_expenses(user_id: int):
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
def update_expense_route(expense_id: int, expense: ExpenseUpdate):
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
