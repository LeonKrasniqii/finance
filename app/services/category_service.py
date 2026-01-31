# app/services/category_service.py
import requests
from typing import List
from app.models.category import CategoryResponse
from config import API_BASE_URL

# --- Get all categories ---
def get_all_categories() -> List[CategoryResponse]:
    url = f"{API_BASE_URL}/categories"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch categories: {resp.text}")
    data = resp.json()
    return [CategoryResponse(**item) for item in data]

# --- Add category ---
def add_category(name: str) -> CategoryResponse:
    url = f"{API_BASE_URL}/categories"
    payload = {"name": name}
    resp = requests.post(url, json=payload)
    if resp.status_code != 201:
        raise Exception(f"Failed to add category: {resp.text}")
    return CategoryResponse(**resp.json())

# --- Delete category ---
def delete_category(category_id: int) -> bool:
    url = f"{API_BASE_URL}/categories/{category_id}"
    resp = requests.delete(url)
    if resp.status_code == 200:
        return True
    return False
