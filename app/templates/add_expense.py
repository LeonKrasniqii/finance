from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import date

from app.services import expense_service
from app.database import get_db
from app.auth import get_current_user

router = APIRouter()

class ExpenseCreate(BaseModel):
    category_id: int
    amount: float = Field(gt=0)
    date: date
    description: str | None = None
    payment_method: str | None = None

@router.post("/expenses", status_code=status.HTTP_201_CREATED)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        result = expense_service.create_expense(
            db=db,
            user_id=current_user.id,
            category_id=expense.category_id,
            amount=expense.amount,
            expense_date=expense.date,
            description=expense.description,
            payment_method=expense.payment_method
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
