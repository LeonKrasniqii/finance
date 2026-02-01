import streamlit as st
import requests
from datetime import date
from config import API_BASE_URL

def show():
    st.title("➕ Add Expense")
    if "user" not in st.session_state:
        st.warning("Please login")
        return

    headers = {"Authorization": f"Bearer {st.session_state.get('access_token')}"}
    
    # Category loading logic
    res = requests.get(f"{API_BASE_URL}/categories", headers=headers)
    cat_map = {c['name']: c['id'] for c in res.json()} if res.status_code == 200 else {}

    cat_name = st.selectbox("Category", list(cat_map.keys()))
    amount = st.number_input("Amount", min_value=0.01)
    desc = st.text_input("Description")
    dt = st.date_input("Date", value=date.today())

    if st.button("Add Expense"):
        payload = {
            "user_id": st.session_state["user"]["id"],
            "category_id": cat_map[cat_name],
            "amount": amount,
            "description": desc,
            "date": dt.isoformat()
        }
        r = requests.post(f"{API_BASE_URL}/expenses/", json=payload, headers=headers)
        if r.status_code == 200: st.success("Added!")
        else: st.error(f"Error: {r.text}")