from src.domains.inventory.services.item_service import create_inventory_item
from src.domains.inventory.persistence.category_db import CategoryDB
from src.domains.inventory.persistence.item_db import ItemDB

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

def test_create_inventory_item_normalize_unit() -> None:
    fake_category = CategoryDB(id=1, name="Meat", perishable_default=True)
    fake_saved_item = ItemDB(id=1, name="Chicken", category_id=1, default_unit="lb")

    with (patch("src.domains.inventory.services.item_service.get_category") as mock_get_category,
          patch("src.domains.inventory.services.item_service.create_item") as mock_create_item):
        mock_get_category.return_value = fake_category
        mock_create_item.return_value = fake_saved_item

        result = create_inventory_item(session=MagicMock(), name="Chicken", category_id=1, default_unit=" LB ")

        assert result.id == 1
        assert result.name == "Chicken"
        assert result.category_id == 1
        assert result.default_unit == "lb"

        saved_domain_item = mock_create_item.call_args.kwargs["item"]

        assert saved_domain_item.name == "Chicken"
        assert saved_domain_item.category_id == 1
        assert saved_domain_item.default_unit == "lb"

def test_create_inventory_item_rejects_unsupported_unit() -> None:
    fake_category = CategoryDB(id=1, name="Meat", perishable_default=True)
    
    with (patch("src.domains.inventory.services.item_service.get_category") as mock_get_category,
          patch("src.domains.inventory.services.item_service.create_item") as mock_create_item):
        mock_get_category.return_value = fake_category

        with pytest.raises(ValueError, match="Unsupported unit"):
            create_inventory_item(session=MagicMock(), name="chicken", category_id=1, default_unit="banana")

        mock_create_item.assert_not_called()

def test_create_inventory_item_rejects_missing_category() -> None:
    with (patch("src.domains.inventory.services.item_service.get_category") as mock_get_category,
          patch("src.domains.inventory.services.item_service.create_item") as mock_create_item):

        mock_get_category.return_value = None

        with pytest.raises(ValueError, match="Category does not exist"):
            create_inventory_item(session=MagicMock(),name="Chicken",category_id=999, default_unit="lb")

        mock_create_item.assert_not_called()