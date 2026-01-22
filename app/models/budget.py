from pydantic import BaseModel, Field
from typing import Optional

# Base model: shared fields
class BudgetBase(BaseModel):
    user_id: int = Field(..., gt=0)
    category_id: int = Field(..., gt=0)
    monthly_limit: float = Field(..., gt=0)

# Model used when creating a budget
class BudgetCreate(BudgetBase):
    pass

# Model returned in responses (with ID)
class BudgetResponse(BudgetBase):
    id: int

# Full model including ID (for internal/domain use)
class Budget(BudgetBase):
    id: int
