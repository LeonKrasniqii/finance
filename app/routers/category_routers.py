from fastapi import APIRouter, HTTPException
from pydantic import BaseModel  # FIXED: BaseModel comes from pydantic
from app.services import category_service

router = APIRouter(prefix="/categories", tags=["Categories"])

class CategoryCreate(BaseModel):
    name: str

@router.get("/")
def list_categories():
    return category_service.get_all_categories()

@router.post("/")
def create_category(data: CategoryCreate):
    new_id = category_service.add_category(data.name)
    return {"id": new_id, "message": "Category created"}


@router.delete("/{category_id}")
def delete_cat(category_id: int):
    success, message = category_service.delete_category(category_id)
    if not success:
        # Sends your custom message back with a 400 error
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}