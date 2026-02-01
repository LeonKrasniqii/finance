from pydantic import BaseModel
from datetime import date

class ExpenseCreate(BaseModel):
    user_id: int
    category_id: int
    amount: float
    description: str
    date: date

class ExpenseResponse(ExpenseCreate):
    id: int

class ExpenseUpdate(BaseModel):
    category_id: int
    amount: float
    description: str
    date: date