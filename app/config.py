import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "dev-secret-key"
    DATABASE = os.path.join(BASE_DIR, "finance.db")
