import streamlit as st
from app.services.expense_service import get_expenses_by_user

def show():
    st.title("📈 Reports")

    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please login first")
        return

    user_id = st.session_state["user"]["id"]
    expenses = get_expenses_by_user(user_id)

    if not expenses:
        st.info("No expenses to report.")
        return

    st.subheader("All Expenses")
    st.table(expenses)
