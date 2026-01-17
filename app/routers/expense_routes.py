from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from app.database.db_connection import get_db_connection
from datetime import datetime

router = APIRouter(prefix="/expenses", tags=["Expenses"])

# Pydantic models for request and response validation
class ExpenseCreate(BaseModel):
    user_id: int
    title: str
    amount: float
    category: Optional[str] = None
    date: Optional[datetime] = None

class ExpenseUpdate(BaseModel):
    title: Optional[str]
    amount: Optional[float]
    category: Optional[str]
    date: Optional[datetime]

class ExpenseResponse(BaseModel):
    id: int
    user_id: int
    title: str
    amount: float
    category: Optional[str]
    date: Optional[datetime]


# Create an expense
@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (user_id, title, amount, category, date)
        VALUES (?, ?, ?, ?, ?)
    """, (expense.user_id, expense.title, expense.amount, expense.category, expense.date))
    
    conn.commit()
    expense_id = cursor.lastrowid
    conn.close()

    return {**expense.dict(), "id": expense_id}


# Get all expenses for a user
@router.get("/user/{user_id}", response_model=List[ExpenseResponse])
def get_user_expenses(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, user_id, title, amount, category, date
        FROM expenses
        WHERE user_id = ?
    """, (user_id,))
    
    expenses = cursor.fetchall()
    conn.close()
    
    return [dict(expense) for expense in expenses]


# Get a single expense
@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, user_id, title, amount, category, date
        FROM expenses
        WHERE id = ?
    """, (expense_id,))
    
    expense = cursor.fetchone()
    conn.close()
    
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    return dict(expense)


# Update an expense
@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build dynamic update query
    update_fields = {k: v for k, v in expense.dict().items() if v is not None}
    
    if not update_fields:
        conn.close()
        raise HTTPException(status_code=400, detail="No fields to update")
    
    set_clause = ", ".join([f"{k} = ?" for k in update_fields.keys()])
    values = list(update_fields.values()) + [expense_id]
    
    cursor.execute(f"""
        UPDATE expenses
        SET {set_clause}
        WHERE id = ?
    """, values)
    
    conn.commit()
    
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    updated_expense = cursor.fetchone()
    conn.close()
    
    if not updated_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    return dict(updated_expense)


# Delete an expense
@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    
    return
