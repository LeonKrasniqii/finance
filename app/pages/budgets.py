import streamlit as st
import requests
from config import API_BASE_URL

def show():
    st.title("🎯 Budget Management")
    
    if "user" not in st.session_state:
        st.error("Please log in first.")
        return

    user_id = st.session_state["user"]["id"]

    # --- SECTION 1: CREATE OR UPDATE BUDGET ---
    st.subheader("Set or Change a Budget")
    
    # Get categories for the dropdown
    cat_resp = requests.get(f"{API_BASE_URL}/categories/")
    categories = cat_resp.json() if cat_resp.status_code == 200 else []
    
    if not categories:
        st.info("No categories found. Please create categories first.")
        return

    cat_options = {c['name']: c['id'] for c in categories}
    
    with st.form("budget_form", clear_on_submit=True):
        selected_cat_name = st.selectbox("Select Category", options=list(cat_options.keys()))
        amount = st.number_input("Monthly Limit ($)", min_value=1.0, step=10.0)
        
        if st.form_submit_button("Save Budget"):
            payload = {
                "user_id": user_id,
                "category_id": cat_options[selected_cat_name],
                "monthly_limit": amount
            }
            res = requests.post(f"{API_BASE_URL}/budgets/{user_id}", json=payload)
            if res.status_code == 200:
                st.success(f"Budget for {selected_cat_name} saved!")
                st.rerun()
            else:
                st.error("Failed to save budget.")

    # --- SECTION 2: VIEW & DELETE EXISTING BUDGETS ---
    st.divider()
    st.subheader("Existing Budgets")
    
    bud_resp = requests.get(f"{API_BASE_URL}/budgets/{user_id}")
    if bud_resp.status_code == 200:
        current_budgets = bud_resp.json()
        
        if not current_budgets:
            st.info("You haven't set any budgets yet.")
        else:
            # Reverse map to get category names from IDs
            id_to_name = {v: k for k, v in cat_options.items()}
            
            for b in current_budgets:
                cat_name = id_to_name.get(b['category_id'], "Unknown")
                
                col1, col2, col3 = st.columns([0.5, 0.3, 0.2])
                with col1:
                    st.write(f"**{cat_name}**")
                with col2:
                    st.write(f"${b['amount']:.2f}")
                with col3:
                    # DELETE BUTTON
                    if st.button("🗑️", key=f"del_bud_{b['category_id']}"):
                        # We send a DELETE request to a new endpoint
                        del_res = requests.delete(f"{API_BASE_URL}/budgets/{user_id}/{b['category_id']}")
                        if del_res.status_code == 200:
                            st.rerun()
                        else:
                            st.error("Could not delete.")
    else:
        st.error("Could not load budgets.")