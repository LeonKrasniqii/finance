import streamlit as st
import requests
from datetime import date
from config import API_BASE_URL

def show():
    st.title("➕ Add Expense")

    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please login first")
        return

    user = st.session_state["user"]
    headers = {
        "x-user-id": str(user["id"]),  # must be string
        "Authorization": f"Bearer {user.get('access_token', '')}"
    }

    # Pre-fill if editing
    edit_expense = st.session_state.get("edit_expense")
    if edit_expense:
        category_id_default = edit_expense["category_id"]
        amount_default = edit_expense["amount"]
        description_default = edit_expense["description"]
        date_default = date.fromisoformat(edit_expense["date"])
    else:
        category_id_default = None
        amount_default = 0.0
        description_default = ""
        date_default = date.today()

    # Fetch categories from API
    try:
        response = requests.get(f"{API_BASE_URL}/categories", headers=headers)
        response.raise_for_status()
        categories = response.json()
        if not categories:
            st.warning("No categories found. Please add categories first.")
            return
    except requests.RequestException as e:
        st.error(f"Failed to fetch categories: {str(e)}")
        return

    category_map = {c["name"]: c["id"] for c in categories}
    category_name_default = next((c["name"] for c in categories if c["id"] == category_id_default), list(category_map.keys())[0])

    category_name = st.selectbox("Category", list(category_map.keys()), index=list(category_map.keys()).index(category_name_default))
    amount = st.number_input("Amount", min_value=0.01, value=float(amount_default))
    description = st.text_input("Description", value=description_default)
    expense_date = st.date_input("Date", value=date_default)

    if st.button("Save Expense"):
        payload = {
            "category_id": category_map[category_name],
            "amount": amount,
            "description": description,
            "date": expense_date.isoformat(),
        }

        try:
            if edit_expense:  # Update existing expense
                resp = requests.put(f"{API_BASE_URL}/expenses/{edit_expense['id']}", json=payload, headers=headers)
            else:  # Add new expense
                resp = requests.post(f"{API_BASE_URL}/expenses", json=payload, headers=headers)

            if resp.status_code in (200, 201):
                st.success("Expense saved successfully ✅")
                if "edit_expense" in st.session_state:
                    del st.session_state["edit_expense"]
                st.experimental_rerun()
            else:
                st.error(f"Failed: {resp.text}")
        except requests.RequestException as e:
            st.error(f"Error connecting to API: {str(e)}")
