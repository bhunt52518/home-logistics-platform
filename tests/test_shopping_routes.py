from unittest.mock import patch
from decimal import Decimal

from fastapi.testclient import TestClient

from src.domains.shopping.persistence.shopping_list_db import ShoppingListItemDB
from src.domains.shopping.models.shopping_list_merge_suggestion import ShoppingListMergeSuggestion
from src.domains.shopping.models.shopping_list_item_response import ShoppingListItemResponse
from src.domains.shopping.models.shopping_list_source import ShoppingListSource
from src.domains.shopping.services.shopping_list_service import add_shopping_list_item, approve_shopping_list_merge_suggestion
from src.main import app



client = TestClient(app)


def test_add_shopping_list_item_adds_item() -> None:
    fake_shopping_list_item = ShoppingListItemDB(
        id=1, item_id=None, name="Birthday Candles", quantity=Decimal("1"), unit="pack",
        source=ShoppingListSource.MANUAL, purchased=False
    )

    with patch("src.api.routes.shopping.shopping.add_shopping_list_item") as mock_add_shopping_list_item:
        mock_add_shopping_list_item.return_value = fake_shopping_list_item

        response = client.post(
            "/shopping/item",
            json={
                "name": "Birthday Candles",
                "quantity": "1",
                "unit": "pack",
                "source": "manual"
            }
        )

        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "item_id": None,
            "name": "Birthday Candles",
            "quantity": "1",
            "unit": "pack",
            "source": "manual",
            "purchased": False
        }

        mock_add_shopping_list_item.assert_called_once()

        kwargs = mock_add_shopping_list_item.call_args.kwargs
        request_sent_to_service = kwargs["shopping_list_item"]

        assert kwargs["session"] is not None
        assert request_sent_to_service.name == "Birthday Candles"
        assert request_sent_to_service.quantity == Decimal("1")
        assert request_sent_to_service.unit == "pack"
        assert request_sent_to_service.source == ShoppingListSource.MANUAL

def test_add_shopping_list_item_returns_merge_suggestion() -> None:
    fake_merge_suggestion = ShoppingListMergeSuggestion(
        shopping_list_item_id=1, name="Chicken", existing_quantity=Decimal("3"), requested_quantity=Decimal("2"),
        merged_quantity=Decimal("5"), unit="lb"
    )

    with patch("src.api.routes.shopping.shopping.add_shopping_list_item") as mock_add_shopping_list_item:
        mock_add_shopping_list_item.return_value = fake_merge_suggestion

        response = client.post(
            "/shopping/item",
            json={
                "name": "Chicken",
                "quantity": "2",
                "unit": "lb",
                "source": "manual"

            }
        )

        assert response.status_code == 200
        assert response.json() == {
            "shopping_list_item_id": 1,
            "name": "Chicken",
            "existing_quantity": "3",
            "requested_quantity": "2",
            "merged_quantity": "5",
            "unit": "lb"
        }

        mock_add_shopping_list_item.assert_called_once()

        kwargs = mock_add_shopping_list_item.call_args.kwargs
        request_sent_to_service = kwargs["shopping_list_item"]

        assert kwargs["session"] is not None
        assert request_sent_to_service.name == "Chicken"
        assert request_sent_to_service.quantity == Decimal("2")
        assert request_sent_to_service.unit == "lb"
        assert request_sent_to_service.source == ShoppingListSource.MANUAL

def test_approve_shopping_list_merge_seggestion_returns_updated_list() -> None:
    fake_updated_shopping_list_item = ShoppingListItemResponse(
        id=1, item_id=1, name="Chicken", quantity=Decimal("5"), unit="lb",
        source=ShoppingListSource.MANUAL, purchased=False
    )

    with patch("src.api.routes.shopping.shopping.approve_shopping_list_merge_suggestion") as mock_approve_shopping_list_merge_suggestion:
        mock_approve_shopping_list_merge_suggestion.return_value = fake_updated_shopping_list_item

        response = client.post(
            "/shopping/merge/approve",
            json={
                "shopping_list_item_id": 1,
                "existing_quantity": "3",
                "requested_quantity": "2",
                "merged_quantity": "5",
                "name": "Chicken",
                "unit": "lb"
            }
        )

        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "item_id": 1,
            "name": "Chicken",
            "quantity": "5",
            "unit": "lb",
            "source": "manual",
            "purchased": False
        }

        mock_approve_shopping_list_merge_suggestion.assert_called_once()
        kwargs = mock_approve_shopping_list_merge_suggestion.call_args.kwargs
        requst_sent_to_service = kwargs["merge_suggestion"]

        assert kwargs["session"] is not None
        assert requst_sent_to_service.shopping_list_item_id == 1
        assert requst_sent_to_service.existing_quantity == Decimal("3")
        assert requst_sent_to_service.requested_quantity == Decimal("2")
        assert requst_sent_to_service.merged_quantity == Decimal("5")
        assert requst_sent_to_service.name == "Chicken"
        assert requst_sent_to_service.unit == "lb"