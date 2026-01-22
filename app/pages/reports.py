import streamlit as st
from app.services.expense_service import get_user_expenses
from app.services.analysis_service import expense_summary

def show():
    st.title("📈 Expense Reports")

    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please login first")
        return

    user_id = st.session_state["user"]["id"]

    # Fetch user expenses
    expenses = get_user_expenses(user_id)

    if not expenses:
        st.info("No expenses to summarize.")
        return

    # Show all expenses
    st.subheader("All Expenses")
    st.table([e.model_dump() for e in expenses])

    # Show summary by category
    st.subheader("Summary by Category")
    summary = expense_summary(expenses)
    st.table([{"Category": cat, "Total Amount": amt} for cat, amt in summary.items()])

    # Optional: show total expenses
    total = sum(summary.values())
    st.write(f"**Total Expenses:** ${total:.2f}")
