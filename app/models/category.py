from pydantic import BaseModel, Field

# Base shared fields
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

# Used when creating a category
class CategoryCreate(CategoryBase):
    pass

# Used when returning a category to the client (includes ID)
class CategoryResponse(CategoryBase):
    id: int

# Full category model (optional, includes ID)
class Category(CategoryBase):
    id: int
