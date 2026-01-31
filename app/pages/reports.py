import streamlit as st
import requests
from config import API_BASE_URL

def show():
    st.title("📈 Expense Reports")

    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please login first")
        return

    user = st.session_state["user"]
    headers = {
        "x-user-id": str(user["id"]),  # header must be string
        "Authorization": f"Bearer {user.get('access_token', '')}"
    }

    # Fetch user expenses from API
    try:
        response = requests.get(f"{API_BASE_URL}/expenses/me", headers=headers, timeout=10)

        if response.status_code != 200:
            st.error(f"Failed to fetch expenses: {response.json().get('detail', response.text)}")
            return

        expenses = response.json()
        if not expenses:
            st.info("No expenses to summarize.")
            return

    except requests.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return

    # Show all expenses
    st.subheader("All Expenses")
    st.table(expenses)

    # Summary by category
    st.subheader("Summary by Category")
    summary = {}
    for e in expenses:
        cat = e.get("category_id")
        summary[cat] = summary.get(cat, 0) + float(e.get("amount", 0))

    st.table([{"Category": cat, "Total Amount": amt} for cat, amt in summary.items()])

    # Optional: total
    total = sum(summary.values())
    st.write(f"**Total Expenses:** ${total:.2f}")
