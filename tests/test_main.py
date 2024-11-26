from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

test_receipt_object = {
    "retailer": "M&M Corner Market",
    "purchaseDate": "2021-01-01",
    "purchaseTime": "13:01",
    "items": [{"shortDescription": "Mountain Dew 12PK", "price": 6.49}],
    "total": 6.49,
}


def test_process_receipts():
    with client as c:
        response = c.post("/receipts/process", json=test_receipt_object)
        assert response.status_code == 200
        assert "id" in response.json()
