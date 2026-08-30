from unittest.mock import patch

from fastapi.testclient import TestClient
from decimal import Decimal
from datetime import date

from src.main import app
from src.domains.inventory.persistence.item_db import ItemDB
from src.domains.inventory.models.restock_status_response import RestockStatusResponse
from src.domains.inventory.models.item_quantity_response import ItemQuantityResponse

client = TestClient(app)

def test_post_item_returns_created_item() -> None:
    fake_item = ItemDB(
        id=1,
        category_id=1,
        name="Chicken",
        default_unit="lb",
        restock_point=Decimal("2")
    )

    with patch("src.api.routes.inventory.item.create_inventory_item") as mock_create_inventory_item:
        mock_create_inventory_item.return_value = fake_item

        response = client.post(
            "/inventory/item",
            json={
                "name": "Chicken",
                "category_id": 1,
                "default_unit": "lb",
                "restock_point": "2",
            },
        )

        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "category_id": 1,
            "name": "Chicken",
            "default_unit": "lb",
            "restock_point": "2",
        }

        kwargs = mock_create_inventory_item.call_args.kwargs
        assert kwargs["category_id"] == 1
        assert kwargs["name"] == "Chicken"
        assert kwargs["default_unit"] == "lb"
        assert "session" in kwargs

def test_post_item_rejects_invailid_category() -> None:
    fake_item = ItemDB(
        id=1,
        category_id=1,
        name="Chicken",
        default_unit="lb",
        restock_point= Decimal("2")
    )

    with patch("src.api.routes.inventory.item.create_inventory_item") as mock_create_inventory_item:
        mock_create_inventory_item.side_effect = ValueError("Category does not exist.")

        response = client.post(
                    "/inventory/item",
                    json={
                        "category_id": 999,
                        "name": "Chicken",
                        "default_unit": "lb",
                        "restock_point": "2",
                    },
                )
        
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Category does not exist.",
            }
        
        mock_create_inventory_item.assert_called_once()

        kwargs = mock_create_inventory_item.call_args.kwargs
        assert kwargs["category_id"] == 999

def test_get_item_quaintity_returns_valid_quantity() -> None:
    fake_total_item_quantity = ItemQuantityResponse(
        name="Chicken",
        total_quantity=Decimal("5"),
        unit="lb",
    )

    with patch("src.api.routes.inventory.item.get_item_inventory_quantity") as mock_get_item_quantity:
        mock_get_item_quantity.return_value = fake_total_item_quantity

        response = client.get(
            "/inventory/item/1/quantity",
        )

        assert response.status_code == 200
        assert response.json() == {
            "name": "Chicken",
            "total_quantity": "5",
            "unit": "lb",
        }

        kwargs = mock_get_item_quantity.call_args.kwargs

        assert kwargs["item_id"] == 1
        assert "session" in kwargs

def test_get_item_quaintity_rejects_invalid_item() -> None:

    with patch("src.api.routes.inventory.item.get_item_inventory_quantity") as mock_get_item_quantity:
        mock_get_item_quantity.side_effect = ValueError("Item does not exist.")

        response = client.get(
            "/inventory/item/1/quantity",
        )

        assert response.status_code == 400
        assert response.json() == {
            "detail": "Item does not exist."
        }

        mock_get_item_quantity.assert_called_once()

def test_get_restock_status_returns_valid_status() -> None:
    fake_restock_status = RestockStatusResponse(
        name= "Chicken",
        current_quantity= Decimal("1"),
        restock_point= Decimal("2"),
        unit= "lb",
        needs_restock= True
    )

    with patch("src.api.routes.inventory.item.get_restock_status") as mock_get_restock_status:
        mock_get_restock_status.return_value = fake_restock_status

        response= client.get(
            "/inventory/item/1/restock-status"
        )

        assert response.status_code == 200
        assert response.json() == {
            "name": "Chicken",
            "current_quantity": "1",
            "restock_point": "2",
            "unit": "lb",
            "needs_restock": True
        }
        kwargs = mock_get_restock_status.call_args.kwargs

        assert kwargs["item_id"] == 1
        assert "session" in kwargs

def test_get_restock_status_rejects_missing_item() -> None:

    with patch("src.api.routes.inventory.item.get_restock_status") as mock_get_restock_status:
        mock_get_restock_status.side_effect = ValueError("Item does not exist.")

        response = client.get(
            "/inventory/item/1/restock-status"
        )

        assert response.status_code == 400
        assert response.json() == {
            "detail": "Item does not exist."
        }

        mock_get_restock_status.assert_called_once()

        kwargs = mock_get_restock_status.call_args.kwargs
        assert kwargs["item_id"] == 1
        assert "session" in kwargs

def test_get_all_items_needing_restock_returns_valid_list() -> None:
    fake_response_1 = RestockStatusResponse(name="Chicken", current_quantity=Decimal("2"), restock_point=Decimal("2"), unit="lb", needs_restock=True)
    fake_response_2 = RestockStatusResponse(name="Steak", current_quantity=Decimal("2"), restock_point=Decimal("4"), unit="lb", needs_restock=True)
    fake_response_3 = RestockStatusResponse(name="Milk", current_quantity=Decimal("0"), restock_point=Decimal("0"), unit="gal", needs_restock=True)

    with patch("src.api.routes.inventory.item.get_items_needing_restock") as mock_get_items_needing_restock:
        mock_get_items_needing_restock.return_value = [fake_response_1, fake_response_2, fake_response_3]

        response = client.get(
            "/inventory/item/restock-needed"
        )

        body = response.json()

        assert response.status_code == 200
        assert len(body) == 3

        assert body[0] == {
            "name": "Chicken",
            "current_quantity": "2",
            "restock_point": "2",
            "unit": "lb",
            "needs_restock": True
        }
        assert body[1] == {
            "name": "Steak",
            "current_quantity": "2",
            "restock_point": "4",
            "unit": "lb",
            "needs_restock": True
        }
        assert body[2] == {
            "name": "Milk",
            "current_quantity": "0",
            "restock_point": "0",
            "unit": "gal",
            "needs_restock": True
        }

        kwargs = mock_get_items_needing_restock.call_args.kwargs
        assert "session" in kwargs

def test_get_all_items_needing_restock_returns_empty_list() -> None:
    with patch("src.api.routes.inventory.item.get_items_needing_restock") as mock_get_items_needing_restock:
        mock_get_items_needing_restock.return_value = []

        response = client.get(
            "/inventory/item/restock-needed"
        )
        assert response.status_code == 200
        assert response.json() == []

        kwargs = mock_get_items_needing_restock.call_args.kwargs
        assert "session" in kwargs