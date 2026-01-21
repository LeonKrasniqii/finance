import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Reports")

st.title("📈 Expense Reports")

user_id = st.number_input("User ID", min_value=1)

if st.button("Generate Report"):
    response = requests.get(f"http://127.0.0.1:8000/reports/expenses/{user_id}")
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(list(data.items()), columns=["Category", "Total"])
        st.bar_chart(df.set_index("Category"))
    else:
        st.error("Could not generate report")
