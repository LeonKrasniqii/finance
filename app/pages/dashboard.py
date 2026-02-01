import streamlit as st
import requests
import pandas as pd
from config import API_BASE_URL

def show():
    st.title("📊 Personal Dashboard")
    
    if "user" not in st.session_state:
        st.error("Please login.")
        return

    user_id = st.session_state["user"]["id"]

    try:
        # ADDED ?user_id= here to satisfy the backend
        response = requests.get(f"{API_BASE_URL}/expenses/me?user_id={user_id}")
        
        if response.status_code == 200:
            expenses = response.json()
            if expenses:
                df = pd.DataFrame(expenses)
                st.metric("Total Spent", f"${df['amount'].sum():,.2f}")
                st.subheader("Recent Activity")
                st.dataframe(df.tail(5), use_container_width=True, hide_index=True)
            else:
                st.info("No expenses found.")
        else:
            st.error(f"Error {response.status_code}")
    except Exception as e:
        st.error(f"Dashboard connection failed: {e}")