import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/auth"  # FastAPI auth router

def show():
    st.title("🔐 Login")

    # Initialize session state
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "token" not in st.session_state:
        st.session_state["token"] = None
    if "_rerun_flag" not in st.session_state:
        st.session_state["_rerun_flag"] = 0

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button", use_container_width=True):
        if not username or not password:
            st.error("Please enter both username and password")
            return

        try:
            response = requests.post(
                f"{API_URL}/login",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                data = response.json()
                st.session_state["user"] = data["user"]
                st.session_state["token"] = data.get("access_token", None)

                st.success(f"Logged in successfully ✅ Welcome, {username}")

                # Modern way to force rerun: toggle a dummy session_state key
                st.session_state["_rerun_flag"] += 1

            else:
                st.error(response.json().get("detail", "Login failed"))

        except Exception as e:
            st.error(f"Error connecting to server: {e}")

    # Force rerun when _rerun_flag changes
    _ = st.session_state.get("_rerun_flag")
