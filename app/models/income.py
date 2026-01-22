from pydantic import BaseModel, Field
from datetime import date

class IncomeBase(BaseModel):
    user_id: int = Field(..., gt=0)
    source: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    date: date

class IncomeCreate(IncomeBase):
    pass

class IncomeResponse(IncomeBase):
    id: int

class Income(IncomeBase):
    id: int
