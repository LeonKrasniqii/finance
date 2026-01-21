import streamlit as st
import requests

st.set_page_config(page_title="Register")

st.title("📝 Register")

username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Register"):
    response = requests.post(
        "http://127.0.0.1:8000/auth/register",
        params={
            "username": username,
            "email": email,
            "password": password
        }
    )

    if response.status_code == 200:
        st.success("Account created. Please login.")
        st.switch_page("templates/login.py")
    else:
        st.error("Registration failed")
