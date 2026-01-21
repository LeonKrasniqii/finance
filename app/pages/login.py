import streamlit as st
from app.services.auth_service import login_user

def show():
    st.title("Login")

    if "user" not in st.session_state:
        st.session_state["user"] = None

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        if not username or not password:
            st.error("Please enter both username and password")
            return

        user = login_user(username, password)
        if user:
            st.session_state["user"] = dict(user)
            st.success("Logged in successfully")
            st.rerun()
        else:
            st.error("Invalid credentials")
