from pydantic import BaseModel, Field
from datetime import date

class ExpenseBase(BaseModel):
    user_id: int = Field(..., gt=0)
    category_id: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)
    description: str = Field(..., min_length=1, max_length=255)
    date: date

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    id: int

class Expense(ExpenseBase):
    id: int
