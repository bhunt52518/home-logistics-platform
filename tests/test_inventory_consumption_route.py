from datetime import date
from decimal import Decimal
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.domains.inventory.persistence.inventory_record_db import (
    InventoryRecordDB,
)
from src.domains.inventory.services.inventory_consumption_service import consume_inventory
from src.main import app


client = TestClient(app)


def test_post_inventory_consumption_returns_updated_record() -> None:
    fake_updated_record = InventoryRecordDB(
        id=1,
        item_id=1,
        location_id=1,
        quantity=Decimal("7"),
        unit="lb",
        purchase_date=date(2026, 5, 26),
        expiration_date=None,
    )

    with patch(
        "src.api.routes.inventory.consumption.consume_inventory"
    )as mock_consume_inventory:
        mock_consume_inventory.return_value = fake_updated_record

        response = client.post(
            "/inventory/consume",
            json={
                "inventory_record_id": 1,
                "quantity": 3,
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "item_id": 1,
        "location_id": 1,
        "quantity": "7",
        "unit": "lb",
        "purchase_date": "2026-05-26",
        "expiration_date": None,
    }

    mock_consume_inventory.assert_called_once()

    kwargs = mock_consume_inventory.call_args.kwargs
    request_sent_to_service = kwargs["consumption_request"]

    assert kwargs["session"] is not None
    assert request_sent_to_service.inventory_record_id == 1
    assert request_sent_to_service.quantity == Decimal("3")


def test_post_inventory_consumption_returns_400_for_missing_record() -> None:
    with patch(
        "src.api.routes.inventory.consumption.consume_inventory"
    ) as mock_consume_inventory:
        mock_consume_inventory.side_effect = ValueError(
            "Record does not exist."
        )

        response = client.post(
            "/inventory/consume",
            json={
                "inventory_record_id": 999,
                "quantity": 3,
            },
        )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Record does not exist.",
    }

    mock_consume_inventory.assert_called_once()


def test_post_inventory_consumption_returns_400_when_quantity_exceeds_inventory() -> None:
    with patch(
        "src.api.routes.inventory.consumption.consume_inventory"
    ) as mock_consume_inventory:
        mock_consume_inventory.side_effect = ValueError(
            "Consumption amount can not exceed inventory quantity"
        )

        response = client.post(
            "/inventory/consume",
            json={
                "inventory_record_id": 1,
                "quantity": 20,
            },
        )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Consumption amount can not exceed inventory quantity",
    }

    mock_consume_inventory.assert_called_once()


def test_post_inventory_consumption_rejects_non_positive_quantity() -> None:
    with patch(
        "src.api.routes.inventory.consumption.consume_inventory"
    ) as mock_consume_inventory:
        response = client.post(
            "/inventory/consume",
            json={
                "inventory_record_id": 1,
                "quantity": 0,
            },
        )

    assert response.status_code == 422
    mock_consume_inventory.assert_not_called()