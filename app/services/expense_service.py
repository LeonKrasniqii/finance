from app.models.expense import create_expense, get_expenses_by_user

def add_expense(data, user_id):
    return create_expense(
        user_id=user_id,
        category_id=data["category_id"],
        amount=data["amount"],
        expense_date=data["expense_date"],
        description=data.get("description"),
        payment_method=data.get("payment_method")
    )

def list_expenses(user_id):
    return get_expenses_by_user(user_id)
