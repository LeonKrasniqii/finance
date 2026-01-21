import streamlit as st
import requests

st.set_page_config(page_title="Dashboard")

st.title("📊 Dashboard")

if "token" not in st.session_state:
    st.warning("Please login first")
    st.stop()

user_id = st.number_input("Your User ID", min_value=1)

if st.button("View Expenses"):
    response = requests.get(f"http://127.0.0.1:8000/expenses/{user_id}")
    if response.status_code == 200:
        st.table(response.json())
