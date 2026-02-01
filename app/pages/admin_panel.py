import streamlit as st
import requests
from config import API_BASE_URL

def show():
    st.title("👑 Admin Control Panel")
    token = st.session_state.get("access_token")

    if not token:
        st.error("No admin token found.")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # --- FETCH USERS ---
    try:
        response = requests.get(f"{API_BASE_URL}/admin/users", headers=headers)
        if response.status_code == 200:
            users = response.json()
            
            # --- CREATE TABLE HEADER ---
            cols = st.columns([1, 2, 3, 2, 3])
            cols[0].write("**ID**")
            cols[1].write("**Username**")
            cols[2].write("**Email**")
            cols[3].write("**Role**")
            cols[4].write("**Actions**")
            st.divider()

            # --- RENDER USER ROWS ---
            for user in users:
                c1, c2, c3, c4, c5 = st.columns([1, 2, 3, 2, 3])
                c1.write(user["id"])
                c2.write(user["username"])
                c3.write(user["email"])
                c4.write(user["role"])

                # --- DELETE ACTION ---
                # We use a unique key for every button using the user ID
                if c5.button("🗑️ Delete", key=f"del_{user['id']}", type="secondary"):
                    del_res = requests.delete(f"{API_BASE_URL}/admin/users/{user['id']}", headers=headers)
                    if del_res.status_code == 200:
                        st.success(f"User {user['username']} deleted!")
                        st.rerun()
                    else:
                        st.error("Failed to delete user.")

        else:
            st.error("Could not load users.")
    except Exception as e:
        st.error(f"Error: {e}")