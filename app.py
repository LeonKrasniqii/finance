import streamlit as st
from app.database.db_init import init_db
from app.pages import login, register, dashboard, add_expense, reports, categories, admin_panel, budgets 

# Initialize database once
init_db()

st.set_page_config(page_title="Finance App", layout="wide")

# Session defaults
if "user" not in st.session_state:
    st.session_state["user"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None

# Sidebar navigation
st.sidebar.title("💰 Finance Tracker")

choice = None

if st.session_state["user"]:
    # 1. Define menu options - Added 'Budgets' here!
    menu_options = ["Dashboard", "Add Expense", "Budgets", "Categories", "Reports"]
    
    # 2. Add Admin Panel if role is admin
    if st.session_state.get("role") == "admin":
        menu_options.append("👑 Admin Panel")
    
    menu_options.append("Logout")
    
    choice = st.sidebar.radio("Go to", menu_options)
else:
    choice = st.sidebar.radio("Go to", ["Login", "Register"])

# --- ROUTING LOGIC ---
if choice == "Login":
    login.show()
elif choice == "Register":
    register.show()
elif choice == "Dashboard":
    dashboard.show()
elif choice == "Add Expense":
    add_expense.show()
elif choice == "Budgets":  # <--- Added routing for Budgets
    budgets.show()
elif choice == "Categories":
    categories.show()
elif choice == "Reports":
    reports.show()
elif choice == "👑 Admin Panel":
    admin_panel.show()
elif choice == "Logout":
    st.session_state["user"] = None
    st.session_state["role"] = None
    st.session_state["access_token"] = None
    st.success("Logged out")
    st.rerun()