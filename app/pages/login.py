import streamlit as st
import requests

st.set_page_config(page_title="Login")

st.title("🔐 Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    response = requests.post(
        "http://127.0.0.1:8000/auth/login",
        params={"username": username, "password": password}
    )

    if response.status_code == 200:
        token = response.json()["access_token"]
        st.success("Login successful")
        st.session_state["token"] = token
        st.switch_page("templates/dashboard.py")
    else:
        st.error("Invalid credentials")
