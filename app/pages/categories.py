import streamlit as st
import requests
from config import API_BASE_URL

def show():
    st.title("📁 Category Management")

    # --- Section: Add Category ---
    with st.expander("➕ Add New Category"):
        new_cat_name = st.text_input("Category Name")
        if st.button("Save Category"):
            if new_cat_name:
                res = requests.post(f"{API_BASE_URL}/categories/", json={"name": new_cat_name})
                if res.status_code == 200:
                    st.success("Category added!")
                    st.rerun()
                else:
                    st.error("Failed to add category.")

    st.divider()

    # --- Section: List and Delete ---
    try:
        response = requests.get(f"{API_BASE_URL}/categories/")
        if response.status_code == 200:
            categories = response.json()
            
            if not categories:
                st.info("No categories available.")
            else:
                # Add a header for clarity
                h1, h2 = st.columns([4, 1])
                h1.markdown("### Category Name & [ID]")
                h2.markdown("### Action")
                
                for cat in categories:
                    col1, col2 = st.columns([4, 1])
                    
                    # DISPLAY FIX: Showing the ID in brackets next to the name
                    # This gives you the number you need for your Swagger DELETE requests
                    cat_id = cat['id']
                    cat_name = cat['name']
                    col1.markdown(f"**{cat_name}** `[ID: {cat_id}]` ")
                    
                    if col2.button("🗑️", key=f"cat_{cat_id}", use_container_width=True):
                        del_res = requests.delete(f"{API_BASE_URL}/categories/{cat_id}")
                        if del_res.status_code == 200:
                            st.success(f"Deleted {cat_name}!")
                            st.rerun()
                        else:
                            # If it's used in reports, this will show the "Cannot delete" error
                            error_detail = del_res.json().get('detail', 'Error')
                            st.error(f"{error_detail}")
        else:
            st.error("Failed to load categories from server.")
    except Exception as e:
        st.error(f"Connection Error: {e}")