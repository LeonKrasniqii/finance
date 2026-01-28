from fastapi import APIRouter, HTTPException, Depends, Header
from app.database.db_connection import get_db_connection
from app.models.user import UserResponse
from app.models.expense import ExpenseResponse
from typing import List
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from app.routers.auth_routes import decode_access_token


SECRET_KEY = "your_secret_key_here"  # Replace with your actual secret key
ALGORITHM = "HS256"

router = APIRouter(prefix="/admin", tags=["Admin"])

# --- Helper to extract token from Authorization header ---
def get_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    return authorization.split(" ")[1]


# --- Decode JWT token ---
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# --- Dependency to enforce admin role ---
def admin_required(token: str = Depends(get_token)):
    payload = decode_token(token)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload

# --- Routes ---
@router.get("/users", response_model=List[UserResponse])
def get_all_users(payload: dict = Depends(admin_required)):
    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute("SELECT id, username, email, role FROM users")
        users = cursor.fetchall()
    return [UserResponse(id=u[0], username=u[1], email=u[2], role=u[3]) for u in users]

@router.get("/expenses", response_model=List[ExpenseResponse])
def get_all_expenses(payload: dict = Depends(admin_required)):
    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT id, user_id, category_id, amount, description, date
            FROM expenses
        """)
        expenses = cursor.fetchall()
    return [
        ExpenseResponse(
            id=e[0],
            user_id=e[1],
            category_id=e[2],
            amount=e[3],
            description=e[4],
            date=e[5]
        ) for e in expenses
    ]

@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, payload: dict = Depends(admin_required)):
    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Expense not found")
        db.commit()
    return {"message": "Expense deleted successfully"}
