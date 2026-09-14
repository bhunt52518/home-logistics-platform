from src.domains.shopping.services.shopping_list_service import (
    add_shopping_list_item, get_duplicate_shopping_list_item, create_shopping_list_item, approve_shopping_list_merge_suggestion,
    get_active_shopping_list, mark_shopping_list_item_as_purchased, get_purchased_items, stock_purchased_item, complete_purchased_item)
from src.domains.shopping.persistence.shopping_list_db import ShoppingListItemDB
from src.domains.shopping.models.shopping_list_source import ShoppingListSource
from src.domains.shopping.models.shopping_list_item import ShoppingListItem
from src.domains.shopping.models.shopping_list_merge_suggestion import ShoppingListMergeSuggestion
from src.domains.shopping.models.stock_purchased_items_request import StockPurchasedItemRequest
from src.domains.inventory.persistence.inventory_record_db import InventoryRecordDB
from src.domains.inventory.models.inventory_allocation import InventoryAllocation

from unittest.mock import MagicMock
from unittest.mock import patch
from decimal import Decimal
from datetime import date

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

def test_get_active_shopping_list_returns_valid_list() -> None:
    fake_session = MagicMock()
    item_1 = ShoppingListItemDB(
        id=1, item_id=1, name="Chicken", quantity=Decimal("3"), unit="lb",
        source=ShoppingListSource.RESTOCK, purchased=False)
    item_2 = ShoppingListItemDB(
        id=2, item_id=2, name="Milk", quantity=Decimal("2"), unit="gal",
        source=ShoppingListSource.RESTOCK, purchased=False)


    with patch("src.domains.shopping.services.shopping_list_service.get_active_shopping_list_items") as mock_get_active_shopping_list_items:
        mock_get_active_shopping_list_items.return_value = [item_1, item_2]

        result = get_active_shopping_list(session=fake_session)

        assert len(result) == 2
        mock_get_active_shopping_list_items.assert_called_once()

def test_mark_shopping_list_item_as_purchased() -> None:
    fake_session = MagicMock()
    fake_updated_item = ShoppingListItemDB(
        id=1, item_id=1, name="Chicken", quantity=Decimal("3"), unit="lb",
        source=ShoppingListSource.RESTOCK, purchased=True)

    with patch("src.domains.shopping.services.shopping_list_service.update_shopping_list_item_as_purchased") as mock_update_item:
        mock_update_item.return_value = fake_updated_item

        result = mark_shopping_list_item_as_purchased(session=fake_session, shopping_list_item_id=1)

        assert result.purchased is True
        assert result.item_id == 1

def test_get_purchased_items_returns_valid_list() -> None:
    fake_session = MagicMock()
    item_1 = ShoppingListItemDB(
        id=1, item_id=1, name="Chicken", quantity=Decimal("3"), unit="lb",
        source=ShoppingListSource.RESTOCK, purchased=True)
    item_2 = ShoppingListItemDB(
        id=2, item_id=2, name="Milk", quantity=Decimal("2"), unit="gal",
        source=ShoppingListSource.RESTOCK, purchased=True)


    with patch("src.domains.shopping.services.shopping_list_service.get_purchased_shopping_list_items") as mock_get_purchased_items:
        mock_get_purchased_items.return_value = [item_1, item_2]

        result = get_purchased_items(session=fake_session)

        assert len(result) == 2
        mock_get_purchased_items.assert_called_once()

        kwargs = mock_get_purchased_items.call_args.kwargs
        assert kwargs["session"] is fake_session

def test_stock_purchase_item_returns_valid_stocked_item() -> None:
    fake_session = MagicMock()
    fake_stocked_item = ShoppingListItemDB(
        item_id=1, name="Chicken", quantity=Decimal("5"), unit="lb", source=ShoppingListSource.RESTOCK,
        purchased=True, stocked=True)
    fake_shopping_list_item = ShoppingListItemDB(
        item_id=1, name="Chicken", quantity=Decimal("5"), unit= "lb", source=ShoppingListSource.RESTOCK,
        purchased=True, stocked=False)
    fake_stock_request =  StockPurchasedItemRequest(
         allocations=[InventoryAllocation(location_id=1, quantity=Decimal("2")),
                      InventoryAllocation(location_id=2, quantity=Decimal("3"))])

    with (patch("src.domains.shopping.services.shopping_list_service.get_shopping_list_item") as mock_get_shopping_list_item,
          patch("src.domains.shopping.services.shopping_list_service.process_allocation") as mock_process_allocation,
          patch("src.domains.shopping.services.shopping_list_service.update_shopping_list_item_as_stocked") as mock_update_shopping_list_item_as_stocked):
        mock_get_shopping_list_item.return_value = fake_shopping_list_item
        mock_process_allocation.return_value = []
        mock_update_shopping_list_item_as_stocked.return_value = fake_stocked_item

        result = stock_purchased_item(session=fake_session, shopping_list_item_id=1, stock_request=fake_stock_request)

        assert result.stocked is True
        mock_process_allocation.assert_called_once()
        mock_update_shopping_list_item_as_stocked.assert_called_once()
        mock_process_allocation.assert_called_once()

        allocation_request = mock_process_allocation.call_args.kwargs["allocation_request"]
        assert allocation_request.item_id == 1
        assert allocation_request.purchased_quantity == Decimal("5")
        assert allocation_request.item_unit == "lb"
        assert allocation_request.allocations == fake_stock_request.allocations

def test_stock_purchase_item_returns_error_for_no_item() -> None:
    fake_session = MagicMock()
    fake_stock_request =  StockPurchasedItemRequest(
        allocations=[InventoryAllocation(location_id=1, quantity=Decimal("2")),
                     InventoryAllocation(location_id=2, quantity=Decimal("3"))])

    with patch("src.domains.shopping.services.shopping_list_service.get_shopping_list_item") as mock_get_shopping_list_item:
        mock_get_shopping_list_item.return_value = None

        with pytest.raises(ValueError) as error:
            stock_purchased_item(session=fake_session, shopping_list_item_id=1, stock_request=fake_stock_request)

            assert str(error.value) == "Shopping list item does not exist."

def test_stock_purchase_item_returns_error_for_Item_not_purchased() -> None:
    fake_session = MagicMock()
    fake_shopping_list_item = ShoppingListItemDB(
            item_id=1, name="Chicken", quantity=Decimal("5"), unit= "lb", source=ShoppingListSource.RESTOCK,
            purchased=False, stocked=False)
    fake_stock_request =  StockPurchasedItemRequest(
        allocations=[InventoryAllocation(location_id=1, quantity=Decimal("2")),
                     InventoryAllocation(location_id=2, quantity=Decimal("3"))])

    with patch("src.domains.shopping.services.shopping_list_service.get_shopping_list_item") as mock_get_shopping_list_item:
        mock_get_shopping_list_item.return_value = fake_shopping_list_item

        with pytest.raises(ValueError) as error:
            stock_purchased_item(session=fake_session, shopping_list_item_id=1, stock_request=fake_stock_request)

            assert str(error.value) == "Shopping list item has not be purchased."

def test_stock_purchase_item_returns_error_for_Item_already_stocked() -> None:
    fake_session = MagicMock()
    fake_shopping_list_item = ShoppingListItemDB(
            item_id=1, name="Chicken", quantity=Decimal("5"), unit= "lb", source=ShoppingListSource.RESTOCK,
            purchased=True, stocked=True)
    fake_stock_request =  StockPurchasedItemRequest(
        allocations=[InventoryAllocation(location_id=1, quantity=Decimal("2")),
                     InventoryAllocation(location_id=2, quantity=Decimal("3"))])

    with patch("src.domains.shopping.services.shopping_list_service.get_shopping_list_item") as mock_get_shopping_list_item:
        mock_get_shopping_list_item.return_value = fake_shopping_list_item

        with pytest.raises(ValueError) as error:
            stock_purchased_item(session=fake_session, shopping_list_item_id=1, stock_request=fake_stock_request)

            assert str(error.value) == "Shopping item has already been stocked."

def test_stock_purchase_item_returns_error_for_Item_not_in_inventory() -> None:
    fake_session = MagicMock()
    fake_shopping_list_item = ShoppingListItemDB(
            item_id=None, name=str, quantity=Decimal("5"), unit= "lb", source=ShoppingListSource.RESTOCK,
            purchased=True, stocked=True)
    fake_stock_request =  StockPurchasedItemRequest(
        allocations=[InventoryAllocation(location_id=1, quantity=Decimal("2")),
                     InventoryAllocation(location_id=2, quantity=Decimal("3"))])

    with patch("src.domains.shopping.services.shopping_list_service.get_shopping_list_item") as mock_get_shopping_list_item:
        mock_get_shopping_list_item.return_value = fake_shopping_list_item

        with pytest.raises(ValueError) as error:
            stock_purchased_item(session=fake_session, shopping_list_item_id=1, stock_request=fake_stock_request)

            assert str(error.value) == "Shopping list item is not linked to an inventory item."

def test_stock_purchase_item_returns_error_for_allocation_not_matching() -> None:
    fake_session = MagicMock()
    fake_shopping_list_item = ShoppingListItemDB(
        item_id=1, name="Chicken", quantity=Decimal("5"), unit= "lb", source=ShoppingListSource.RESTOCK,
        purchased=True, stocked=False)
    fake_stock_request =  StockPurchasedItemRequest(
         allocations=[InventoryAllocation(location_id=1, quantity=Decimal("3")),
                      InventoryAllocation(location_id=2, quantity=Decimal("3"))])

    with (patch("src.domains.shopping.services.shopping_list_service.get_shopping_list_item") as mock_get_shopping_list_item,
        patch("src.domains.shopping.services.shopping_list_service.process_allocation") as mock_process_allocation,
        patch("src.domains.shopping.services.shopping_list_service.update_shopping_list_item_as_stocked") as mock_update_shopping_list_item_as_stocked):

        mock_get_shopping_list_item.return_value = fake_shopping_list_item
        mock_process_allocation.side_effect = ValueError("Allocation quantity does not equal purchased quantity.")

        with pytest.raises(ValueError) as error:
            stock_purchased_item(
            session=fake_session,
            shopping_list_item_id=1,
            stock_request=fake_stock_request
            )

        assert str(error.value) == "Allocation quantity does not equal purchased quantity."

        mock_update_shopping_list_item_as_stocked.assert_not_called()
        mock_process_allocation.assert_called_once()

def test_complete_purchased_item_returns_item_true() -> None:
    fake_session = MagicMock()
    fake_shopping_list_item = ShoppingListItemDB(
        id=1, item_id=None, name="Chicken", quantity=Decimal("5"), unit= "lb", source=ShoppingListSource.MANUAL,
        purchased=True, stocked=False, completed=False)
    fake_completed_shopping_list_item = ShoppingListItemDB(
        id=1, item_id=None, name="Chicken", quantity=Decimal("5"), unit= "lb", source=ShoppingListSource.MANUAL,
        purchased=True, stocked=False, completed=True)
    

    with (patch("src.domains.shopping.services.shopping_list_service.get_shopping_list_item") as mock_get_shopping_list_item,
        patch("src.domains.shopping.services.shopping_list_service.update_shopping_list_item_as_completed") as mock_completed_item):
        mock_get_shopping_list_item.return_value = fake_shopping_list_item
        mock_completed_item.return_value = fake_completed_shopping_list_item

        result = complete_purchased_item(
            session=fake_session, shopping_list_item_id=fake_shopping_list_item.id)

        assert result.completed == True
        assert result.id == 1
        mock_completed_item.assert_called_once()
        mock_get_shopping_list_item.assert_called_once()

def test_complete_purchase_item_returns_error_for_no_item() -> None:
    fake_session = MagicMock()

    with patch("src.domains.shopping.services.shopping_list_service.get_shopping_list_item") as mock_get_shopping_list_item:
        mock_get_shopping_list_item.return_value = None

        with pytest.raises(ValueError) as error:
            complete_purchased_item(session=fake_session, shopping_list_item_id=1)

            assert str(error.value) == "Shopping list item does not exist."

def test_complete_purchase_item_returns_error_for_having_item_id() -> None:
    fake_session = MagicMock()
    fake_shopping_list_item = ShoppingListItemDB(
        id=1, item_id=1, name="Chicken", quantity=Decimal("5"), unit= "lb", source=ShoppingListSource.MANUAL,
        purchased=True, stocked=False, completed=False)

    with patch("src.domains.shopping.services.shopping_list_service.get_shopping_list_item") as mock_get_shopping_list_item:
        mock_get_shopping_list_item.return_value = fake_shopping_list_item

        with pytest.raises(ValueError) as error:
            complete_purchased_item(session=fake_session, shopping_list_item_id=1)

            assert str(error.value) == "Shopping list item already exist in inventory."

def test_complete_purchase_item_returns_error_not_putchased() -> None:
    fake_session = MagicMock()
    fake_shopping_list_item = ShoppingListItemDB(
        id=1, item_id=None, name="Chicken", quantity=Decimal("5"), unit= "lb", source=ShoppingListSource.MANUAL,
        purchased=False, stocked=False, completed=False)

    with patch("src.domains.shopping.services.shopping_list_service.get_shopping_list_item") as mock_get_shopping_list_item:
        mock_get_shopping_list_item.return_value = fake_shopping_list_item

        with pytest.raises(ValueError) as error:
            complete_purchased_item(session=fake_session, shopping_list_item_id=1)

            assert str(error.value) == "Shopping list item has not been purchased."

def test_complete_purchase_item_returns_error_already_completed() -> None:
    fake_session = MagicMock()
    fake_shopping_list_item = ShoppingListItemDB(
        id=1, item_id=None, name="Chicken", quantity=Decimal("5"), unit= "lb", source=ShoppingListSource.MANUAL,
        purchased=True, stocked=False, completed=True)

    with patch("src.domains.shopping.services.shopping_list_service.get_shopping_list_item") as mock_get_shopping_list_item:
        mock_get_shopping_list_item.return_value = fake_shopping_list_item

        with pytest.raises(ValueError) as error:
            complete_purchased_item(session=fake_session, shopping_list_item_id=1)

            assert str(error.value) == "Shopping list item has already been completed."
    



        




