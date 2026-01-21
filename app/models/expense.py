# app/models/expense.py

class Expense:
    """
    Expense model
    """

    def __init__(
        self,
        id: int,
        user_id: int,
        category_id: int,
        amount: float,
        description: str,
        date: str
    ):
        self.id = id
        self.user_id = user_id
        self.category_id = category_id
        self.amount = amount
        self.description = description
        self.date = date

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "amount": self.amount,
            "description": self.description,
            "date": self.date
        }
