from app.database.db_connection import get_db
from app.models.budget import BudgetCreate, BudgetResponse
from fastapi import HTTPException
from typing import List


# --- Set or update a budget ---
def set_budget(budget: BudgetCreate) -> BudgetResponse:
    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO budgets (user_id, category_id, monthly_limit)
                VALUES (?, ?, ?)
                """,
                (budget.user_id, budget.category_id, budget.monthly_limit)
            )
            db.commit()

            # SQLite doesn't return lastrowid for REPLACE if updating, so we just return the budget
            return BudgetResponse(id=None, **budget.model_dump())  # id can be None or fetch separately
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Get budgets for a user ---
def get_budgets(user_id: int) -> List[BudgetResponse]:
    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "SELECT id, user_id, category_id, monthly_limit FROM budgets WHERE user_id=?", (user_id,)
            )
            rows = cursor.fetchall()

        # Convert raw rows to Pydantic models
        return [
            BudgetResponse(id=row[0], user_id=row[1], category_id=row[2], monthly_limit=row[3])
            for row in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
