from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime
from app.database.db_connection import get_db_connection

router = APIRouter(prefix="/reports", tags=["Reports"])


# Get total expenses for a user
@router.get("/total/{user_id}")
def get_total_expenses(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(amount) as total
        FROM expenses
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()
    conn.close()

    total = result["total"] if result["total"] is not None else 0
    return {"user_id": user_id, "total_expenses": total}


# Get total expenses by category
@router.get("/category/{user_id}")
def get_expenses_by_category(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
    """, (user_id,))

    result = cursor.fetchall()
    conn.close()

    return {"user_id": user_id, "category_totals": [dict(row) for row in result]}


# Get expenses within a date range
@router.get("/range/{user_id}")
def get_expenses_in_date_range(user_id: int, start_date: str, end_date: str):
    """
    Dates should be in YYYY-MM-DD format
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Dates must be YYYY-MM-DD format")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, amount, category, date
        FROM expenses
        WHERE user_id = ? AND date BETWEEN ? AND ?
        ORDER BY date ASC
    """, (user_id, start_date, end_date))

    expenses = cursor.fetchall()
    conn.close()

    return {
        "user_id": user_id,
        "start_date": start_date,
        "end_date": end_date,
        "expenses": [dict(row) for row in expenses]
    }


# Get monthly summary
@router.get("/monthly/{user_id}")
def get_monthly_expenses(user_id: int, year: Optional[int] = None):
    """
    Returns total expenses per month.
    If year is not provided, defaults to current year.
    """
    if not year:
        year = datetime.now().year

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT strftime('%m', date) as month, SUM(amount) as total
        FROM expenses
        WHERE user_id = ? AND strftime('%Y', date) = ?
        GROUP BY month
        ORDER BY month ASC
    """, (user_id, str(year)))

    result = cursor.fetchall()
    conn.close()

    return {
        "user_id": user_id,
        "year": year,
        "monthly_totals": [dict(row) for row in result]
    }
