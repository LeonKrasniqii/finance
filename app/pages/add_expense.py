import streamlit as st
import requests
from datetime import date

st.set_page_config(page_title="Add Expense")

st.title("➕ Add Expense")

user_id = st.number_input("User ID", min_value=1)
category_id = st.number_input("Category ID", min_value=1)
amount = st.number_input("Amount", min_value=0.01)
description = st.text_input("Description")
expense_date = st.date_input("Date", value=date.today())

if st.button("Add Expense"):
    response = requests.post(
        "http://127.0.0.1:8000/expenses/",
        params={
            "user_id": user_id,
            "category_id": category_id,
            "amount": amount,
            "description": description,
            "date": expense_date.isoformat()
        }
    )

    if response.status_code == 200:
        st.success("Expense added")
    else:
        st.error("Failed to add expense")
