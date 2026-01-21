# app/services/analysis_service.py

from collections import defaultdict


def expense_summary(expenses):
    summary = defaultdict(float)
    for e in expenses:
        summary[e.category_id] += e.amount
    return dict(summary)
