from unittest.mock import patch

from fastapi.testclient import TestClient
from decimal import Decimal
from datetime import date

from src.main import app
from src.domains.inventory.persistence.item_db import ItemDB
from src.domains.inventory.persistence.category_db import CategoryDB
from src.domains.inventory.models.item_quantity_response import ItemQuantityResponse

client = TestClient(app)

def test_post_item_returns_created_item() -> None:
    fake_item = ItemDB(
        id=1,
        category_id=1,
        name="Chicken",
        default_unit="lb",
    )

    with patch("src.api.routes.inventory.item.create_inventory_item") as mock_create_inventory_item:
        mock_create_inventory_item.return_value = fake_item

        response = client.post(
            "/inventory/item",
            json={
                "name": "Chicken",
                "category_id": 1,
                "default_unit": "lb",
            },
        )

        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "category_id": 1,
            "name": "Chicken",
            "default_unit": "lb"
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
    )

    with patch("src.api.routes.inventory.item.create_inventory_item") as mock_create_inventory_item:
        mock_create_inventory_item.side_effect = ValueError("Category does not exist.")

        response = client.post(
                    "/inventory/item",
                    json={
                        "category_id": 999,
                        "name": "Chicken",
                        "default_unit": "lb"
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

