from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_inventory_alloctions_check() -> None:
    request_body = {
    "item_id": 37,
    "purchased_quantity": "10",
    "item_unit": "lb",
    "allocations": [
        {
            "location_id": 1,
            "quantity": "2",
        },
        {
            "location_id": 2,
            "quantity": "8",
        },
    ],
}
    response = client.post(
    "/inventory/allocations",
    json=request_body,
)
    assert response.status_code == 200

    body = response.json()

    assert body["item_id"] == 37
    assert body["purchased_quantity"] == "10"
    assert body["allocations"][0]["location_id"] == 1
    assert body["allocations"][1]["quantity"] == "8"