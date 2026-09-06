from src.domains.shopping.services.shopping_list_service import add_shopping_list_item, get_duplicate_shopping_list_item
from src.domains.shopping.services.shopping_list_service import create_shopping_list_item, approve_shopping_list_merge_suggestion
from src.domains.shopping.persistence.shopping_list_db import ShoppingListItemDB
from src.domains.shopping.models.shopping_list_source import ShoppingListSource
from src.domains.shopping.models.shopping_list_item import ShoppingListItem
from src.domains.shopping.models.shopping_list_merge_suggestion import ShoppingListMergeSuggestion

from unittest.mock import MagicMock
from unittest.mock import patch
from decimal import Decimal

import pytest





def test_add_shoping_list_item_duplicate_returns_none() -> None:
    fake_session = MagicMock()
    fake_shoping_list_item = ShoppingListItem(
        name="Chicken", quantity=Decimal("2"), unit="lb", source=ShoppingListSource.MANUAL, item_id=None,
        purchased=False
    )

    with (patch("src.domains.shopping.services.shopping_list_service.get_duplicate_shopping_list_item") as mock_get_duplicate_shopping_list_item,
          patch("src.domains.shopping.services.shopping_list_service.create_shopping_list_item") as mock_create_shopping_list_item):
        mock_get_duplicate_shopping_list_item.return_value = None
        mock_create_shopping_list_item.return_value = fake_shoping_list_item

        result = add_shopping_list_item(session=fake_session, shopping_list_item=fake_shoping_list_item)

        assert result.name =="Chicken"
        assert result.quantity == Decimal("2")
        assert result.unit =="lb"
        assert result.source == ShoppingListSource.MANUAL
        assert result.item_id is None
        assert result.purchased is False

        mock_get_duplicate_shopping_list_item.assert_called_once()
        mock_create_shopping_list_item.assert_called_once_with(
            session=fake_session, shopping_list=fake_shoping_list_item
        )

def test_add_shopping_list_item_returns_merge_suggestion() -> None:
    fake_session = MagicMock()
    fake_shoping_list_item = ShoppingListItem(
        name="Chicken", quantity=Decimal("2"), unit="lb", source=ShoppingListSource.MANUAL, item_id=None,
        purchased=False
    )
    fake_shoping_list_db = ShoppingListItemDB(name="Chicken", quantity=Decimal("3"), unit="lb", source=ShoppingListSource.RESTOCK,
        item_id=1, purchased=False
    )

    with (patch("src.domains.shopping.services.shopping_list_service.get_duplicate_shopping_list_item") as mock_get_duplicate_shopping_list_item,
          patch("src.domains.shopping.services.shopping_list_service.create_shopping_list_item") as mock_create_shopping_list_item):
        mock_get_duplicate_shopping_list_item.return_value = fake_shoping_list_db

        result = add_shopping_list_item(session=fake_session, shopping_list_item=fake_shoping_list_item)

        assert result.name =="Chicken"
        assert result.shopping_list_item_id == 1
        assert result.existing_quantity == Decimal("3")
        assert result.requested_quantity == Decimal("2")
        assert result.merged_quantity == Decimal("5")
        assert result.unit == "lb"

        mock_get_duplicate_shopping_list_item.assert_called_once()
        mock_create_shopping_list_item.assert_not_called()
        assert isinstance(result, ShoppingListMergeSuggestion)

def test_approve_shopping_list_merge_suggestion_updates_quantity() -> None:
    fake_session = MagicMock()
    fake_existing_db_item = ShoppingListItemDB(
        item_id =1, name="Chicken", quantity=Decimal("3"), unit="lb", source=ShoppingListSource.RESTOCK,
        purchased=False
    )
    fake_merge_suggestion = ShoppingListMergeSuggestion(
        shopping_list_item_id=1, existing_quantity=Decimal("3"), requested_quantity=Decimal("2"), merged_quantity=Decimal("5"),
        name="Chicken", unit="lb"
    )
    fake_updated_db_item = ShoppingListItemDB(item_id =1, name="Chicken", quantity=Decimal("5"), unit="lb", source=ShoppingListSource.RESTOCK,
            purchased=False
    )

    with (patch("src.domains.shopping.services.shopping_list_service.get_shopping_list_item") as mock_get_shopping_list_item,
        patch("src.domains.shopping.services.shopping_list_service.update_shopping_list_quantity") as mock_update_shopping_list_quantity):
        mock_get_shopping_list_item.return_value = fake_existing_db_item
        mock_update_shopping_list_quantity.return_value = fake_updated_db_item

        result = approve_shopping_list_merge_suggestion(session=fake_session, merge_suggestion=fake_merge_suggestion)

        assert result.quantity== Decimal("5")
        assert result.item_id == 1

        mock_update_shopping_list_quantity.assert_called_once_with(
            session=fake_session, shopping_list=fake_existing_db_item, quantity=Decimal("5")
        )

def test_approve_shopping_list_merge_suggestion_rejects_nonexisting_item() -> None:
    fake_session = MagicMock()
    fake_merge_suggestion = ShoppingListMergeSuggestion(
        shopping_list_item_id=1, existing_quantity=Decimal("3"), requested_quantity=Decimal("2"), merged_quantity=Decimal("5"),
        name="Chicken", unit="lb"
    )
    fake_updated_db_item = ShoppingListItemDB(
        item_id =1, name="Chicken", quantity=Decimal("5"), unit="lb", source=ShoppingListSource.RESTOCK,
        purchased=False
    )
    with (patch("src.domains.shopping.services.shopping_list_service.get_shopping_list_item") as mock_get_shopping_list_item,
            patch("src.domains.shopping.services.shopping_list_service.update_shopping_list_quantity") as mock_update_shopping_list_quantity):
            mock_get_shopping_list_item.return_value = None
            mock_update_shopping_list_quantity.return_value = fake_updated_db_item

            with pytest.raises(ValueError, match="Shopping list item does not exist."):
                 approve_shopping_list_merge_suggestion(session=fake_session, merge_suggestion=fake_merge_suggestion)

                 mock_update_shopping_list_quantity.assert_not_called()

def test_approve_shopping_list_merge_suggestion_rejects_existing_item_quantity_change_before_merge() -> None:
    fake_session = MagicMock()
    fake_existing_db_item = ShoppingListItemDB(
        item_id =1, name="Chicken", quantity=Decimal("3"), unit="lb", source=ShoppingListSource.RESTOCK,
        purchased=False
    )
    fake_merge_suggestion = ShoppingListMergeSuggestion(
        shopping_list_item_id=1, existing_quantity=Decimal("4"), requested_quantity=Decimal("2"), merged_quantity=Decimal("5"),
        name="Chicken", unit="lb"
    )
    fake_updated_db_item = ShoppingListItemDB(item_id =1, name="Chicken", quantity=Decimal("5"), unit="lb", source=ShoppingListSource.RESTOCK,
            purchased=False
    )

    with (patch("src.domains.shopping.services.shopping_list_service.get_shopping_list_item") as mock_get_shopping_list_item,
            patch("src.domains.shopping.services.shopping_list_service.update_shopping_list_quantity") as mock_update_shopping_list_quantity):
            mock_get_shopping_list_item.return_value = fake_existing_db_item
            mock_update_shopping_list_quantity.return_value = fake_updated_db_item

            with pytest.raises(ValueError, match="Existing quantity does not match."):
                 approve_shopping_list_merge_suggestion(session=fake_session, merge_suggestion=fake_merge_suggestion)

                 mock_update_shopping_list_quantity.assert_not_called()




