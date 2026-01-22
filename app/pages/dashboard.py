import streamlit as st
from app.services.expense_service import get_user_expenses

def show():
    st.title("📊 Dashboard")

    # Check if user is logged in
    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please login first")
        return

    user_id = st.session_state["user"]["id"]

    # Fetch expenses using the updated service
    expenses = get_user_expenses(user_id)

    if not expenses:
        st.info("No expenses found.")
        return

    # Convert Pydantic models to dicts for Streamlit table
    expenses_data = [e.model_dump() for e in expenses]

    st.subheader("Your Expenses")
    st.table(expenses_data)
