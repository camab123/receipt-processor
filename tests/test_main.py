from fastapi.testclient import TestClient

from api.main import app
from schemas.receipt import Receipt

client = TestClient(app)

test_receipt_object = {
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
        {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
        {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
        {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
        {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"},
    ],
    "total": "35.35",
}

test_receipt_2 = {
    "retailer": "M&M Corner Market",
    "purchaseDate": "2022-03-20",
    "purchaseTime": "14:33",
    "items": [
        {"shortDescription": "Gatorade", "price": "2.25"},
        {"shortDescription": "Gatorade", "price": "2.25"},
        {"shortDescription": "Gatorade", "price": "2.25"},
        {"shortDescription": "Gatorade", "price": "2.25"},
    ],
    "total": "9.00",
}


def test_process_receipts():
    with client as c:
        response = c.post("/receipts/process", json=test_receipt_object)
        assert response.status_code == 200
        assert "id" in response.json()


def test_get_points():
    with client as c:
        response = c.post("/receipts/process", json=test_receipt_object)
        assert response.status_code == 200
        assert "id" in response.json()
        id = response.json()["id"]
        response = c.get(f"/receipts/{id}/points")
        assert response.status_code == 200
        assert "points" in response.json()
        assert response.json()["points"] == 28


def test_points_function():
    receipt = Receipt(**test_receipt_2)
    assert receipt.get_points() == 109
