from src.domains.shopping.models.shopping_list_item import ShoppingListItem
from src.domains.shopping.models.shopping_list_source import ShoppingListSource
from src.domains.shopping.models.shopping_list_merge_suggestion import ShoppingListMergeSuggestion

from decimal import Decimal
from pydantic import ValidationError

import pytest




def test_shopping_list_item_accepts_valid_item() -> None:
    request_body = {"name": "Birthday Candles", "quantity": "1", "unit": "pack", "source": "manual"}

    shopping_list_item = ShoppingListItem(**request_body)

    assert shopping_list_item.item_id == None
    assert shopping_list_item.name == "Birthday Candles"
    assert shopping_list_item.quantity == Decimal("1")
    assert shopping_list_item.unit == "pack"
    assert shopping_list_item.purchased == False
    assert shopping_list_item.source == ShoppingListSource.MANUAL

def test_shopping_list_item_rejects_zero_quantity() -> None:
    request_body = {"name": "Birthday Candles", "quantity": "0", "unit": "pack", "source": "manual"}

    with pytest.raises(ValidationError):
        ShoppingListItem(**request_body)

def test_shopping_list_item_rejects_negative_quantity() -> None:
    request_body = {"name": "Birthday Candles", "quantity": "-1", "unit": "pack", "source": "manual"}

    with pytest.raises(ValidationError):
        ShoppingListItem(**request_body)

def test_shopping_list_merge_accepts_vaild_merge() -> None:
    request_body = {"shopping_list_item_id": 1, "existing_quantity": "2", "requested_quantity": "1", "merged_quantity": "3", "name": "Chicken", "unit": "lb"}

    shopping_list_merge = ShoppingListMergeSuggestion(**request_body)

    assert shopping_list_merge.shopping_list_item_id == 1
    assert shopping_list_merge.existing_quantity == Decimal("2")
    assert shopping_list_merge.requested_quantity == Decimal("1")
    assert shopping_list_merge.merged_quantity == Decimal("3")
    assert shopping_list_merge.name == "Chicken"
    assert shopping_list_merge.unit == "lb"

def test_shopping_list_merge_suggestion_rejects_negative_quantity() -> None:
    request_body = {"shopping_list_item_id": 1, "existing_quantity": "2", "requested_quantity": "-1", "merged_quantity": "3", "name": "Chicken", "unit": "lb"}

    with pytest.raises(ValidationError):
        ShoppingListMergeSuggestion(**request_body)

def test_shopping_list_merge_suggestion_rejects_zero_quantity() -> None:
    request_body = {"shopping_list_item_id": 1, "existing_quantity": "2", "requested_quantity": "0", "merged_quantity": "3", "name": "Chicken", "unit": "lb"}

    with pytest.raises(ValidationError):
        ShoppingListMergeSuggestion(**request_body)