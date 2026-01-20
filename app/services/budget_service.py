
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.budget import Budget
from app.models.expense import Expense

from database.db_connection import get_db_connection


def create_budget(
    db: Session,
    user_id:int,
    category_id: int,
    amount: float,
    start_date: date,
    end_date: date
):
    
    if amount <= 0:
        raise ValueError("budget amount must be positive")
    
    existing_budget = db.query(Budget).filter(
        Budget.user_id == user_id,
        Budget.category_id == category_id,
        Budget.start_date <= end_date,
        Budget.end_date >= start_date
    ).first()

    if existing_budget:
        raise ValueError("Overlapping budget already exists")

    budget = Budget(
        user_id=user_id,
        category_id=category_id,
        amount=amount,
        start_date=start_date,
        end_date=end_date
    )

    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget

def get_budgets_by_user(db: Session, user_id: int):
    budgets = db.query(Budget).filter(
        Budget.user_id == user_id
    ).all()

    response = []

    for budget in budgets:
        spent = db.query(
            func.coalesce(func.sum(Expense.amount), 0)
        ).filter(
            Expense.user_id == user_id,
            Expense.category_id == budget.category_id,
            Expense.date >= budget.start_date,
            Expense.date <= budget.end_date
        ).scalar()

        response.append({
            "budget_id": budget.id,
            "category_id": budget.category_id,
            "budget_amount": budget.amount,
            "spent": spent,
            "remaining": budget.amount - spent,
            "start_date": budget.start_date,
            "end_date": budget.end_date
        })

    return response

def get_budget_status(db: Session, budget_id: int):
    budget = db.query(Budget).filter(
        Budget.id == budget_id
    ).first()

    if not budget:
        raise ValueError("Budget not found")

    spent = db.query(
        func.coalesce(func.sum(Expense.amount), 0)
    ).filter(
        Expense.user_id == budget.user_id,
        Expense.category_id == budget.category_id,
        Expense.date >= budget.start_date,
        Expense.date <= budget.end_date
    ).scalar()

    return {
        "budget_amount": budget.amount,
        "spent": spent,
        "remaining": budget.amount - spent,
        "percentage_used": round(
            (spent / budget.amount) * 100, 2
        ) if budget.amount > 0 else 0
    }


def update_budget(
    db: Session,
    budget_id: int,
    amount: float | None = None,
    start_date: date | None = None,
    end_date: date | None = None
):
    budget = db.query(Budget).filter(
        Budget.id == budget_id
    ).first()

    if not budget:
        raise ValueError("Budget not found")

    if amount is not None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        budget.amount = amount

    if start_date is not None:
        budget.start_date = start_date

    if end_date is not None:
        budget.end_date = end_date

    db.commit()
    db.refresh(budget)
    return budget



def delete_budget(db: Session, budget_id: int):
    budget = db.query(Budget).filter(
        Budget.id == budget_id
    ).first()

    if not budget:
        raise ValueError("Budget not found")

    db.delete(budget)
    db.commit()
    return True



def is_budget_exceeded(
    db: Session,
    user_id: int,
    category_id: int
):
    today = date.today()

    budget = db.query(Budget).filter(
        Budget.user_id == user_id,
        Budget.category_id == category_id,
        Budget.start_date <= today,
        Budget.end_date >= today
    ).first()

    if not budget:
        return False

    spent = db.query(
        func.coalesce(func.sum(Expense.amount), 0)
    ).filter(
        Expense.user_id == user_id,
        Expense.category_id == category_id,
        Expense.date >= budget.start_date,
        Expense.date <= budget.end_date
    ).scalar()

    return spent > budget.amount

