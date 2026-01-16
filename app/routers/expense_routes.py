from flask import Blueprint, request, jsonify
from app.services.expense_service import add_expense, list_expenses

expense_bp = Blueprint("expenses", __name__)

@expense_bp.route("/expenses", methods=["POST"])
def create():
    user_id = 1  # later from auth
    add_expense(request.json, user_id)
    return jsonify({"message": "Expense added"}), 201

@expense_bp.route("/expenses", methods=["GET"])
def get_all():
    user_id = 1
    expenses = list_expenses(user_id)
    return jsonify([dict(row) for row in expenses])
