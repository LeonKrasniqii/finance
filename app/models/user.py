# app/models/user.py

class User:
    """
    User domain model (OOP)
    """

    def __init__(self, id: int, username: str, email: str, role: str = "user"):
        self.id = id
        self.username = username
        self.email = email
        self.role = role

    def is_admin(self) -> bool:
        return self.role == "admin"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role
        }
