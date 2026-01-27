import streamlit as st
from app.services.auth_service import login_user
from fastapi import HTTPException

def show():
    st.title("🔐 Login")

    if "user" not in st.session_state:
        st.session_state["user"] = None

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button", use_container_width=True):
        if not username or not password:
            st.error("Please enter both username and password")
            return

        try:
            user = login_user(username, password)

            st.session_state["user"] = {
                "id": user.id,
                "username": user.username,
            }

            st.success("Logged in successfully ✅")
            st.rerun()

        except HTTPException as e:
            st.error(e.detail)

        except Exception:
            st.error("Something went wrong. Please try again.")
