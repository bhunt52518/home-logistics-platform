from src.domains.inventory.models.item_create import ItemCreate

from pydantic import ValidationError

import pytest





def test_item_create_accepts_valid_item() -> None:
    request_body = {"name": "Chicken", "category_id": 1, "default_unit": "lb", "restock_point": 2}

    item = ItemCreate(**request_body)

    assert item.name == "Chicken"
    assert item.category_id == 1
    assert item.default_unit == "lb"
    assert item.restock_point == 2

def test_item_create_rejects_invalid_name() -> None:
    with pytest.raises(ValidationError):
        ItemCreate(name="  ") 

def test_item_create_accepts_none_restock_point() -> None:
    request_body = {"name": "Chicken", "category_id": 1, "default_unit": "lb", "restock_point": None}

    item = ItemCreate(**request_body)

    assert item.name == "Chicken"
    assert item.category_id == 1
    assert item.default_unit == "lb"
    assert item.restock_point == None

def test_item_create_accepts_zero_restock_point() -> None:
    request_body = {"name": "Chicken", "category_id": 1, "default_unit": "lb", "restock_point": 0}

    item = ItemCreate(**request_body)

    assert item.name == "Chicken"
    assert item.category_id == 1
    assert item.default_unit == "lb"
    assert item.restock_point == 0

def test_item_create_rejects_invaild_restock_point() -> None:
    request_body = {"name": "Chicken", "category_id": 1, "default_unit": "lb", "restock_point": -1}

    with pytest.raises(ValidationError):
        ItemCreate(**request_body)