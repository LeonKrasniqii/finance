import streamlit as st
import requests
from config import API_BASE_URL, API_TIMEOUT

def show():
    st.title("📂 Categories")

    # Add new category
    new_category = st.text_input("New Category")
    if st.button("Add Category"):
        if new_category.strip():
            try:
                response = requests.post(
                    f"{API_BASE_URL}/categories",
                    json={"name": new_category.strip()},
                    timeout=API_TIMEOUT
                )
                if response.status_code == 201:
                    st.success("Category added successfully ✅")
                    # Instead of experimental_rerun, just reload the categories list
                else:
                    st.error(f"Failed to add category: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to API: {e}")

    # Display existing categories
    categories_container = st.container()  # container will update each run
    try:
        response = requests.get(f"{API_BASE_URL}/categories", timeout=API_TIMEOUT)
        if response.status_code == 200:
            categories = response.json()
            if categories:
                categories_container.subheader("Existing Categories")
                categories_container.table([{"ID": c["id"], "Name": c["name"]} for c in categories])

                for c in categories:
                    if categories_container.button(f"Delete {c['name']}"):
                        try:
                            del_resp = requests.delete(
                                f"{API_BASE_URL}/categories/{c['id']}", timeout=API_TIMEOUT
                            )
                            if del_resp.status_code == 200:
                                st.success(f"Category {c['name']} deleted ✅")
                                # just break the loop to refresh on next run
                                break
                            else:
                                st.error(f"Failed to delete: {del_resp.text}")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Error connecting to API: {e}")
            else:
                categories_container.info("No categories yet.")
        else:
            st.error(f"Failed to fetch categories: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
