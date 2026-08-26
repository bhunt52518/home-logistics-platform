from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError
from decimal import Decimal
from datetime import date

from src.domains.inventory.persistence.inventory_record_db import InventoryRecordDB
from src.domains.inventory.persistence.item_db import ItemDB
from src.domains.inventory.repositories.inventory_repository import get_item, get_inventory_record_by_item
from src.domains.inventory.services.item_inventory_quantity_service import get_item_inventory_quantity




def test_item_inventory_quantity_returns_vailid_quantity() -> None:
    fake_session = MagicMock()
    fake_item_record = ItemDB(id=1, name="chicken", category_id=1, default_unit="lb")
    fake_inventory_record_1 = InventoryRecordDB(id=1, item_id=1, location_id=1, quantity=Decimal("2"), unit="lb",
                                                purchase_date=date(2026,8,1), expiration_date=None)
    fake_inventory_record_2 = InventoryRecordDB(id=2, item_id=1, location_id=2, quantity=Decimal("3"), unit="lb",
                                                    purchase_date=date(2026,8,1), expiration_date=None)
    fake_inventory_by_item = [fake_inventory_record_1, fake_inventory_record_2]

    with (patch("src.domains.inventory.services.item_inventory_quantity_service.get_item") as mock_get_item,
          patch("src.domains.inventory.services.item_inventory_quantity_service.get_inventory_record_by_item") as mock_get_inventory_record_by_item):
        mock_get_item.return_value = fake_item_record
        mock_get_inventory_record_by_item.return_value = fake_inventory_by_item

        result = get_item_inventory_quantity(session=fake_session, item_id=1)

        assert result.name == "chicken"
        assert result.total_quantity == Decimal("5")
        assert result.unit == "lb"
        mock_get_item.assert_called_once()
        mock_get_inventory_record_by_item.assert_called_once()

def test_item_inventory_quantity_returns_zero() -> None:
    fake_session = MagicMock()
    fake_item_record = ItemDB(id=1, name="chicken", category_id=1, default_unit="lb")
    fake_inventory_by_item = []

    with (patch("src.domains.inventory.services.item_inventory_quantity_service.get_item") as mock_get_item,
              patch("src.domains.inventory.services.item_inventory_quantity_service.get_inventory_record_by_item") as mock_get_inventory_record_by_item):
            mock_get_item.return_value = fake_item_record
            mock_get_inventory_record_by_item.return_value = fake_inventory_by_item
    
            result = get_item_inventory_quantity(session=fake_session, item_id=1)
    
            assert result.name == "chicken"
            assert result.total_quantity == Decimal("0")
            assert result.unit == "lb"
            mock_get_item.assert_called_once()
            mock_get_inventory_record_by_item.assert_called_once()

def test_item_inventory_quantity_rejects_missing_item() -> None:
    fake_session = MagicMock()
    fake_item_record = []
    fake_inventory_by_item = []

    with (patch("src.domains.inventory.services.item_inventory_quantity_service.get_item") as mock_get_item,
              patch("src.domains.inventory.services.item_inventory_quantity_service.get_inventory_record_by_item") as mock_get_inventory_record_by_item):
            mock_get_item.return_value = None

    
            with pytest.raises(ValueError, match="Item does not exist."):
                        get_item_inventory_quantity(session=fake_session, item_id=1)
            mock_get_inventory_record_by_item.assert_not_called()