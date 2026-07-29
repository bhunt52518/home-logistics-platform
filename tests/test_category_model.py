from src.domains.inventory.models.category_create import CategoryCreate

from pydantic import ValidationError

import pytest




def test_category_create_accepts_valid_name() -> None:
    request_body = {"name": "Chicken", "perishable_default": True}

    category = CategoryCreate(**request_body)

    assert category.name == "Chicken"
    assert category.perishable_default == True

def test_category_create_rejects_invalid_name() -> None:
    with pytest.raises(ValidationError):
        CategoryCreate(name="  ")   