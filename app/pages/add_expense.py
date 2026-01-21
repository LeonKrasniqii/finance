import streamlit as st
from datetime import date
from app.services.expense_service import add_expense
from app.services.category_service import get_all_categories

def show():
    st.title("➕ Add Expense")

    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please login first")
        return

    categories = get_all_categories()

    if not categories:
        st.warning("No categories found. Please add categories first.")
        return

    category_map = {c.name: c.id for c in categories}

    category_name = st.selectbox("Category", list(category_map.keys()))
    amount = st.number_input("Amount", min_value=0.01)
    description = st.text_input("Description")
    expense_date = st.date_input("Date", value=date.today())

    if st.button("Add Expense"):
        add_expense(
            st.session_state["user"]["id"],
            category_map[category_name],
            amount,
            description,
            expense_date.isoformat()
        )
        st.success("Expense added successfully ✅")
