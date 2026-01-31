import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/auth"  # auth prefix

def show():
    st.title("📝 Register")

    username = st.text_input("Username", key="register_username")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register", key="register_button", use_container_width=True):
        if not username or not email or not password:
            st.error("All fields are required")
            return

        try:
            response = requests.post(
                f"{API_URL}/register",
                json={"username": username, "email": email, "password": password}
            )

            if response.status_code in (200, 201):
                data = response.json()
                st.success(f"Account created successfully ✅ Welcome, {data['user']['username']}")
            else:
                st.error(response.json().get("detail", "Registration failed"))

        except Exception as e:
            st.error(f"Error connecting to server: {e}")
