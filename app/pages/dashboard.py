import streamlit as st
import requests
from config import API_BASE_URL

def show():
    st.title("📊 Dashboard")

    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please login first")
        return

    user = st.session_state["user"]
    headers = {
        "x-user-id": str(user["id"]),  # must be string for headers
        "Authorization": f"Bearer {user.get('access_token', '')}"
    }

    # Fetch expenses from API
    try:
        response = requests.get(f"{API_BASE_URL}/expenses/me", headers=headers, timeout=10)

        if response.status_code != 200:
            st.error(f"Failed to fetch expenses: {response.json().get('detail', response.text)}")
            return

        expenses = response.json()
        if not expenses:
            st.info("No expenses found.")
            return

    except requests.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return

    st.subheader("Your Expenses")
    for expense in expenses:
        st.markdown(
            f"**Category ID:** {expense['category_id']}  |  "
            f"**Amount:** ${expense['amount']:.2f}  |  "
            f"**Date:** {expense['date']}  |  "
            f"**Description:** {expense['description']}"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Edit {expense['id']}", key=f"edit_{expense['id']}"):
                st.session_state["edit_expense"] = expense
                st.experimental_rerun()
        with col2:
            if st.button(f"Delete {expense['id']}", key=f"delete_{expense['id']}"):
                try:
                    del_resp = requests.delete(f"{API_BASE_URL}/expenses/{expense['id']}", headers=headers)
                    if del_resp.status_code == 200:
                        st.success("Expense deleted ✅")
                        st.experimental_rerun()
                    else:
                        st.error(f"Failed to delete: {del_resp.text}")
                except requests.RequestException as e:
                    st.error(f"Error connecting to API: {str(e)}")
