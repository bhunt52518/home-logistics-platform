from fastapi.testclient import TestClient

from src.main import app

from decimal import Decimal

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
    body = response.json()
    assert len(body) == 2

    assert body[0]["item_id"] == 37
    assert body[0]["location_id"] == 1
    assert Decimal(str(body[0]["quantity"])) == Decimal("2")

    assert body[1]["item_id"] == 37
    assert body[1]["location_id"] == 2
    assert Decimal(str(body[1]["quantity"])) == Decimal("8")

    assert response.status_code == 200




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

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Allocation quantity does not equal purchased quantity."
    }
    