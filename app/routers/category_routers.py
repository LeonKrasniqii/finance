from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models.category import CategoryCreate, CategoryResponse
from app.services.category_service import get_all_categories, add_category

router = APIRouter(prefix="/categories", tags=["Categories"])


# --- CREATE ---
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate):
    """
    Add a new category
    """
    try:
        return add_category(category.name)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- READ (all categories) ---
@router.get("/", response_model=List[CategoryResponse])
def read_categories():
    """
    Get all categories
    """
    return get_all_categories()


# --- DELETE ---
@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
def delete_category(category_id: int):
    """
    Delete a category by ID
    """
    try:
        # Use service to delete category (we’ll add delete function next)
        from app.services.category_service import delete_category
        deleted = delete_category(category_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Category not found")
        return {"message": "Category deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
