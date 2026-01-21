# app/models/budget.py

class Budget:
    """
    Budget model
    """

    def __init__(
        self,
        id: int,
        user_id: int,
        category_id: int,
        monthly_limit: float
    ):
        self.id = id
        self.user_id = user_id
        self.category_id = category_id
        self.monthly_limit = monthly_limit

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "monthly_limit": self.monthly_limit
        }
