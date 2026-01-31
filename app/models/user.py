from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: Literal["user", "admin"] = "user"

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

class User(UserBase):
    id: int

    def is_admin(self) -> bool:
        return self.role == "admin"
