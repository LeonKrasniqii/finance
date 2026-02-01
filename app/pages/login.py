import streamlit as st
import requests
from config import API_BASE_URL

def show():
    st.title("🔐 Login")

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", use_container_width=True):
        if not username or not password:
            st.error("Please enter credentials")
            return

        payload = {"username": username, "password": password}

        try:
            response = requests.post(f"{API_BASE_URL}/login", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                # IMPORTANT: Save everything to session_state first
                st.session_state["access_token"] = data.get("access_token")
                st.session_state["user"] = data.get("user")
                st.session_state["role"] = data.get("user", {}).get("role")
                st.session_state["logged_in"] = True # Add this flag
                
                st.success("Logged in! ✅")
                # Instead of st.rerun(), let the main app handle the switch
                st.rerun() 
                
            else:
                st.error(f"Login Failed: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Cannot connect to server. Is server.py running?")