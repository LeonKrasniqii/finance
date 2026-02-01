from fastapi import APIRouter, HTTPException, Query
from app.models.expense import ExpenseCreate
from app.services import expense_service

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.get("/me")
def read_my_expenses(user_id: int = Query(...)):
    # This matches ?user_id= in the URL
    return expense_service.get_user_expenses(user_id)

@router.post("/")
def create_expense(expense: ExpenseCreate):
    new_id = expense_service.add_expense(expense.user_id, expense)
    return {"id": new_id, "message": "Created"}

@router.delete("/{expense_id}")
def remove_expense(expense_id: int, user_id: int = Query(...)):
    success = expense_service.delete_expense(expense_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found or unauthorized")
    return {"message": "Deleted successfully"}