# app/services/category_service.py

from app.database.db_connection import get_db_connection
from app.models.category import CategoryResponse
from fastapi import HTTPException
from typing import List


# --- Get all categories ---
def get_all_categories() -> List[CategoryResponse]:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM categories ORDER BY name")
            rows = cursor.fetchall()

        # Convert rows to Pydantic models
        return [CategoryResponse(id=row[0], name=row[1]) for row in rows]

    except Exception as e:
        # Always raise HTTPException with a readable message
        raise HTTPException(status_code=500, detail=str(e))


# --- Add a new category ---
def add_category(category_name: str) -> CategoryResponse:
    """
    Adds a new category to the database.

    Args:
        category_name (str): Name of the category.

    Returns:
        CategoryResponse: The newly created category.
    """
    # Validate input
    if not category_name or not category_name.strip():
        raise HTTPException(status_code=400, detail="Category name cannot be empty")

    category_name = category_name.strip()

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Insert the category (ignore if it exists)
            cursor.execute(
                "INSERT OR IGNORE INTO categories (name) VALUES (?)",
                (category_name,)
            )
            conn.commit()

            # Fetch the category back
            cursor.execute("SELECT id, name FROM categories WHERE name=?", (category_name,))
            row = cursor.fetchone()
            if row:
                return CategoryResponse(id=row[0], name=row[1])
            else:
                raise HTTPException(status_code=500, detail="Failed to add category")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
