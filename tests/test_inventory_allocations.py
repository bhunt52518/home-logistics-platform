from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_inventory_alloctions_check_is_true() -> None:
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

    assert body["valid"] is True 
    assert body["message"] == "Allocation is valid."

def test_inventory_alloctions_check_is_false() -> None:
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
            "quantity": "5",
        },
    ],
}
    response = client.post(
    "/inventory/allocations",
    json=request_body,
)
    body = response.json()

    assert response.status_code == 200

    assert body["valid"] is False 
    assert body["message"] == "Allocation quantity does not equal purchased quntity."