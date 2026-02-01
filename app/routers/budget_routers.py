from fastapi import APIRouter, HTTPException
from app.models.budget import BudgetCreate
from app.services import budget_service

router = APIRouter(prefix="/budgets", tags=["Budgets"])

@router.post("/{user_id}")
def set_budget(user_id: int, data: BudgetCreate):
    # data.monthly_limit comes from your Pydantic model
    success = budget_service.upsert_budget(
        user_id=user_id, 
        category_id=data.category_id, 
        limit=data.monthly_limit
    )
    if not success:
        raise HTTPException(status_code=500, detail="Database update failed")
    return {"message": "Budget saved"}

@router.get("/{user_id}")
def get_budgets(user_id: int):
    return budget_service.get_user_budgets(user_id)

@router.delete("/{user_id}/{category_id}")
def delete_budget(user_id: int, category_id: int):
    success = budget_service.remove_budget(user_id, category_id)
    if not success:
        raise HTTPException(status_code=400, detail="Delete failed")
    return {"message": "Deleted"}