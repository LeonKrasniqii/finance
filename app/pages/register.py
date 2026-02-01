import streamlit as st
import requests
from config import API_BASE_URL

def show():
    st.title("📝 Register")

    username = st.text_input("Username", key="reg_user")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_pass")

    if st.button("Register", use_container_width=True):
        if not username or not email or not password:
            st.error("Please fill in all fields")
            return

        payload = {
            "username": username, 
            "email": email, 
            "password": password
        }
        
        try:
            response = requests.post(f"{API_BASE_URL}/register", json=payload)
            
            if response.status_code in [200, 201]:
                st.success("Account created! You can now log in.")
                # Optional: clear fields or redirect to login
            else:
                # Get the error message from the JSON response
                error_msg = response.json().get("detail", response.text)
                st.error(f"Registration failed: {error_msg}")
        except Exception as e:
            st.error(f"Connection error: {e}")