import streamlit as st
from app.services.category_service import get_all_categories, add_category, delete_category

def show():
    st.title("📂 Categories")

    # --- Add new category ---
    new_category = st.text_input("New Category", key="new_category_input")
    if st.button("Add Category"):
        if new_category.strip():
            try:
                add_category(new_category.strip())
                st.success(f"Category '{new_category.strip()}' added ✅")
            except Exception as e:
                st.error(f"Failed to add category: {e}")
        else:
            st.warning("Please enter a category name.")

    # --- Display existing categories ---
    categories = get_all_categories()
    if categories:
        st.subheader("Existing Categories")
        for c in categories:
            st.write(f"ID: {c.id} | Name: {c.name}")  # attributes, not dict keys
            if st.button(f"Delete {c.name}", key=f"delete_{c.id}"):
                try:
                    delete_category(c.id)
                    st.success(f"Category '{c.name}' deleted ✅")
                except Exception as e:
                    st.error(f"Failed to delete category: {e}")
    else:
        st.info("No categories yet.")
