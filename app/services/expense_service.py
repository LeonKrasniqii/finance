from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.expense import Expense
from app.services import budget_service

def create_expense(
    db: Session,
    user_id: int,
    category_id: int,
    amount: float,
    expense_date: date,
    description: str | None = None,
    payment_method: str | None = None
):
    # business rule: positive amount
    if amount <= 0:
        raise ValueError("Expense amount must be greater than zero")

    expense = Expense(
        user_id=user_id,
        category_id=category_id,
        amount=amount,
        date=expense_date,
        description=description,
        payment_method=payment_method
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    # 🚨 check if budget exceeded AFTER adding expense
    budget_exceeded = budget_service.is_budget_exceeded(
        db=db,
        user_id=user_id,
        category_id=category_id
    )

    return {
        "expense": expense,
        "budget_exceeded": budget_exceeded
    }
def get_expenses_by_user(
    db: Session,
    user_id: int
):
    return db.query(Expense).filter(
        Expense.user_id == user_id
    ).all()
def get_total_expenses_by_category(
    db: Session,
    user_id: int
):
    return db.query(
        Expense.category_id,
        func.coalesce(func.sum(Expense.amount), 0).label("total_amount")
    ).filter(
        Expense.user_id == user_id
    ).group_by(
        Expense.category_id
    ).all()
def get_total_expenses(
    db: Session,
    user_id: int
):
    return db.query(
        func.coalesce(func.sum(Expense.amount), 0)
    ).filter(
        Expense.user_id == user_id
    ).scalar()
def get_expenses_in_date_range(
    db: Session,
    user_id: int,
    start_date: date,
    end_date: date
):
    return db.query(Expense).filter(
        Expense.user_id == user_id,
        Expense.date >= start_date,
        Expense.date <= end_date
    ).all()
def update_expense(
    db: Session,
    expense_id: int,
    user_id: int,
    data: dict
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == user_id
    ).first()

    if not expense:
        raise ValueError("Expense not found or unauthorized")

    allowed_fields = {
        "amount",
        "category_id",
        "date",
        "description",
        "payment_method"
    }

    for key, value in data.items():
        if key in allowed_fields:
            setattr(expense, key, value)

    db.commit()
    db.refresh(expense)
    return expense
def delete_expense(
    db: Session,
    expense_id: int,
    user_id: int
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == user_id
    ).first()

    if not expense:
        raise ValueError("Expense not found or unauthorized")

    db.delete(expense)
    db.commit()
    return True
