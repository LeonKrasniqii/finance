from app.database.db_connection import get_db_connection
from app.models.category import CategoryCreate, CategoryResponse
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
        raise HTTPException(status_code=500, detail=str(e))


# --- Add a new category ---
def add_category(category: CategoryCreate) -> CategoryResponse:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO categories (name) VALUES (?)",
                (category.name,)
            )
            conn.commit()

            # Return the newly added category
            cursor.execute("SELECT id, name FROM categories WHERE name=?", (category.name,))
            row = cursor.fetchone()
            if row:
                return CategoryResponse(id=row[0], name=row[1])
            else:
                raise HTTPException(status_code=500, detail="Failed to add category")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
