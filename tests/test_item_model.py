from src.domains.inventory.models.item_create import ItemCreate
from src.domains.inventory.models.item_update import ItemUpdate

from pydantic import ValidationError
from decimal import Decimal

import pytest





def test_item_create_accepts_valid_item() -> None:
    request_body = {"name": "Chicken", "category_id": 1, "default_unit": "lb", "restock_point": 2, "target_stock": 5}

    item = ItemCreate(**request_body)

    assert item.name == "Chicken"
    assert item.category_id == 1
    assert item.default_unit == "lb"
    assert item.restock_point == 2
    assert item.target_stock == 5

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

def test_item_create_rejects_invalid_target_stock() -> None:
    request_body = {"name": "Chicken", "category_id": 1, "default_unit": "lb", "restock_point": 2, "target_stock": 0}

    with pytest.raises(ValidationError):
        ItemCreate(**request_body)

def test_item_create_accepts_equal_target_and_restock_points() -> None:
    request_body = {"name": "Chicken", "category_id": 1, "default_unit": "lb", "restock_point": 2, "target_stock": 2}

    item = ItemCreate(**request_body)

    assert item.name == "Chicken"
    assert item.category_id == 1
    assert item.default_unit == "lb"
    assert item.restock_point == 2
    assert item.target_stock == 2

def test_item_update_allows_empty_request() -> None:
    request = ItemUpdate()

    assert request.model_fields_set == set()

def test_item_update_tracks_explicit_none() -> None:
    request = ItemUpdate(restock_point=None)
    assert request.restock_point is None
    assert request.model_fields_set == {"restock_point"}

def test_item_update_rejects_invalid_restock_point() -> None:
    with pytest.raises(ValidationError):
        ItemUpdate(restock_point=Decimal("-1"))

def test_item_update_rejects_invalid_target_stock() -> None:
    with pytest.raises(ValidationError):
        ItemUpdate(target_stock=Decimal("-1"))

def test_item_update_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        ItemUpdate(name="")

