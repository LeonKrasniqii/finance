from collections import defaultdict
from typing import List, Dict
from app.models.expense import ExpenseResponse


def expense_summary(expenses: List[ExpenseResponse]) -> Dict[str, float]:
    """
    Summarizes total expenses per category.

    Args:
        expenses: List of ExpenseResponse objects

    Returns:
        Dictionary mapping category name to total amount
    """
    summary: Dict[str, float] = defaultdict(float)

    for e in expenses:
        # Use category name if available, fallback to category_id
        category_key = getattr(e, "category_name", f"Category {e.category_id}")
        summary[category_key] += e.amount

    return dict(summary)
