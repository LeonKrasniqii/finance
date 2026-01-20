import pandas as pd
from sqlalchemy.orm import Session

def expenses_df(
    db: Session,
    user_id: int
) -> pd.DataFrame:
    query = """
        SELECT
            date,
            amount,
            category_id
        FROM expenses
        WHERE user_id = :user_id
    """

    return pd.read_sql(
        query,
        db.bind,
        params={"user_id": user_id}
    )
def monthly_spending(
    db: Session,
    user_id: int
) -> pd.DataFrame:
    df = expenses_df(db, user_id)

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")

    return (
        df.groupby("month")["amount"]
        .sum()
        .reset_index()
    )
def spending_by_category(
    db: Session,
    user_id: int
) -> pd.DataFrame:
    df = expenses_df(db, user_id)

    return (
        df.groupby("category_id")["amount"]
        .sum()
        .reset_index()
    )
def daily_spending(
    db: Session,
    user_id: int
) -> pd.DataFrame:
    df = expenses_df(db, user_id)

    df["date"] = pd.to_datetime(df["date"])

    return (
        df.groupby("date")["amount"]
        .sum()
        .reset_index()
    )
def budget_vs_actual(
    db: Session,
    user_id: int,
    budgets: list
) -> pd.DataFrame:
    """
    budgets = [
        {"category_id": 1, "amount": 500},
        {"category_id": 2, "amount": 300}
    ]
    """
    expenses = spending_by_category(db, user_id)

    budget_df = pd.DataFrame(budgets)

    return expenses.merge(
        budget_df,
        on="category_id",
        how="left",
        suffixes=("_spent", "_budget")
    )
def overspending_alerts(
    db: Session,
    user_id: int
) -> pd.DataFrame:
    df = spending_by_category(db, user_id)

    df["threshold"] = df["amount"].mean() * 1.5
    return df[df["amount"] > df["threshold"]]
