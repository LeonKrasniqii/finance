import streamlit as st
from app.services.expense_service import get_expenses_by_user

def show():
    st.title("📊 Dashboard")

    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please login first")
        return

    user_id = st.session_state["user"]["id"]

    expenses = get_expenses_by_user(user_id)

    if not expenses:
        st.info("No expenses found.")
        return

    st.subheader("Your Expenses")
    st.table(expenses)
