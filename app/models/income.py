# app/models/income.py

class Income:
    """
    Income model
    """

    def __init__(
        self,
        id: int,
        user_id: int,
        source: str,
        amount: float,
        date: str
    ):
        self.id = id
        self.user_id = user_id
        self.source = source
        self.amount = amount
        self.date = date

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "source": self.source,
            "amount": self.amount,
            "date": self.date
        }
