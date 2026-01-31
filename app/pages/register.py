import streamlit as st
from app.services.auth_service import register_user

def show():
    st.title("Register")

    username = st.text_input("Username", key="register_username")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register", key="register_button"):
        if not username or not email or not password:
            st.error("All fields are required")
            return

        try:
            register_user(username, email, password)
            st.success("Account created successfully. You can now log in.")
        except Exception as e:
            st.error("Username or email already exists")
