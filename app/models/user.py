from pydantic import BaseModel, EmailStr, Field
from typing import Literal

# Base model: shared fields
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: Literal["user", "admin"] = "user"

# Model used when creating a user
class UserCreate(UserBase):
    pass

# Model returned in responses (with ID)
class UserResponse(UserBase):
    id: int

# Full internal model including ID (for domain use)
class User(UserBase):
    id: int

# Domain logic example
    def is_admin(self) -> bool:
        return self.role == "admin"
