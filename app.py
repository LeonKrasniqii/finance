import streamlit as st
from app.database.db_init import init_db
from app.pages import login, register, dashboard, add_expense, reports, categories

# Initialize database once
init_db()

st.set_page_config(page_title="Finance App", layout="wide")

# --- Session defaults ---
if "user" not in st.session_state:
    st.session_state["user"] = None
if "_rerun_flag" not in st.session_state:
    st.session_state["_rerun_flag"] = 0  # dummy flag to force reruns

# --- Sidebar navigation ---
st.sidebar.title("Navigation")

if st.session_state["user"]:
    choice = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Add Expense", "Categories", "Reports", "Logout"]
    )
else:
    choice = st.sidebar.radio(
        "Go to",
        ["Login", "Register"]
    )

# --- Routing ---
if choice == "Login":
    login.show()

elif choice == "Register":
    register.show()

elif choice == "Dashboard":
    dashboard.show()

elif choice == "Add Expense":
    add_expense.show()

elif choice == "Categories":
    categories.show()

elif choice == "Reports":
    reports.show()

elif choice == "Logout":
    st.session_state["user"] = None
    st.success("Logged out ✅")

    # Increment dummy flag to trigger rerun
    st.session_state["_rerun_flag"] += 1

# --- Force rerun if dummy flag changed ---
_ = st.session_state.get("_rerun_flag")
