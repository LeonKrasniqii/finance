from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_expense():
    # You need to get a valid token first - for simplicity here just assume token
    token = "YOUR_TEST_TOKEN"

    headers = {"Authorization": f"Bearer {token}"}
    expense_data = {
        "category_id": 1,
        "amount": 100.0,
        "date": "2026-01-20",
        "description": "Test expense",
        "payment_method": "card"
    }

    response = client.post("/expenses", json=expense_data, headers=headers)
    assert response.status_code == 201
    assert "expense" in response.json()
