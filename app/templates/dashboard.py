import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ==========================
# CONFIG
# ==========================
API_URL = "http://127.0.0.1:8000/api"
TOKEN = ""  # You can login via the app to get a token or implement Streamlit login

headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

# ==========================
# STREAMLIT APP LAYOUT
# ==========================
st.set_page_config(page_title="Expense Dashboard", layout="wide")
st.title("💰 Personal Finance Dashboard")

menu = ["Dashboard", "Expenses", "Reports"]
choice = st.sidebar.selectbox("Menu", menu)

# ==========================
# DASHBOARD PAGE
# ==========================
if choice == "Dashboard":
    st.header("Dashboard Overview")

    # Get dashboard data from FastAPI
    try:
        response = requests.get(f"{API_URL}/dashboard", headers=headers)
        if response.status_code != 200:
            st.warning("Failed to load dashboard. Make sure your FastAPI server is running.")
        else:
            data = response.json()
            budgets = pd.DataFrame(data["budgets"])
            expenses = pd.DataFrame(data["expenses"])
            trend = pd.DataFrame(data["monthly_trend"])

            # Show summary
            st.subheader("Budgets vs Expenses")
            st.dataframe(budgets)
            st.dataframe(expenses)

            # Monthly Trend Chart
            if not trend.empty:
                fig = px.bar(trend, x="month", y="amount", title="Monthly Spending Trend")
                st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")

# ==========================
# EXPENSES PAGE
# ==========================
elif choice == "Expenses":
    st.header("Add New Expense")
    with st.form("expense_form"):
        category_id = st.number_input("Category ID", min_value=1)
        amount = st.number_input("Amount", min_value=0.01, step=0.01)
        expense_date = st.date_input("Date")
        description = st.text_input("Description")
        payment_method = st.selectbox("Payment Method", ["Cash", "Card", "Other"])
        submitted = st.form_submit_button("Add Expense")

        if submitted:
            payload = {
                "category_id": category_id,
                "amount": amount,
                "date": str(expense_date),
                "description": description,
                "payment_method": payment_method
            }
            resp = requests.post(f"{API_URL}/expenses", json=payload, headers=headers)
            if resp.status_code == 201:
                st.success("Expense added successfully!")
            else:
                st.error(f"Failed to add expense: {resp.text}")

# ==========================
# REPORTS PAGE
# ==========================
elif choice == "Reports":
    st.header("Reports Overview")

    try:
        response = requests.get(f"{API_URL}/reports/summary", headers=headers)
        if response.status_code != 200:
            st.warning("Failed to load reports")
        else:
            data = response.json()
            monthly = pd.DataFrame(data["monthly_spending"])
            by_category = pd.DataFrame(data["spending_by_category"])

            st.subheader("Monthly Spending")
            if not monthly.empty:
                fig1 = px.line(monthly, x="month", y="amount", title="Monthly Spending")
                st.plotly_chart(fig1, use_container_width=True)

            st.subheader("Spending by Category")
            if not by_category.empty:
                fig2 = px.pie(by_category, names="category_id", values="amount", title="Spending by Category")
                st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")
