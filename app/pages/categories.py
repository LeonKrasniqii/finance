import streamlit as st
from app.services.category_service import get_all_categories, add_category

def show():
    st.title("📂 Categories")

    new_category = st.text_input("New Category")

    if st.button("Add Category"):
        if new_category.strip():
            add_category(new_category.strip())
            st.success("Category added")
            st.rerun()

    categories = get_all_categories()

    if categories:
        st.subheader("Existing Categories")
        st.table(
            [{"ID": c.id, "Name": c.name} for c in categories]
        )
    else:
        st.info("No categories yet.")
