from src.domains.inventory.services.restock_item_service import get_restock_status
from src.domains.inventory.persistence.item_db import ItemDB
from src.domains.inventory.models.item_quantity_response import ItemQuantityResponse
from src.domains.inventory.models.restock_status_response import RestockStatusResponse

from unittest.mock import MagicMock
from unittest.mock import patch

from datetime import date
from decimal import Decimal

import pytest




def test_get_restock_status_returns_false_when_above_restock_point() -> None:
    fake_session = MagicMock()
    fake_item = ItemDB(id=1, name="Chicken", category_id=1, default_unit="lb", restock_point=Decimal("2"))
    fake_quantity_response = ItemQuantityResponse(name="Chicken", total_quantity=Decimal("6"), unit="lb")

    with (patch("src.domains.inventory.services.restock_item_service.get_item") as mock_get_item,
          patch("src.domains.inventory.services.restock_item_service.get_item_inventory_quantity") as mock_get_item_inventory_quantity):
        mock_get_item.return_value = fake_item
        mock_get_item_inventory_quantity.return_value = fake_quantity_response

        result = get_restock_status(session=fake_session, item_id=fake_item.id)

        assert result.needs_restock == False
        assert result.name == "Chicken"
        assert result.current_quantity == Decimal("6")
        assert result.restock_point == Decimal("2")
        assert result.unit == "lb"

def test_get_restock_status_returns_true_when_equal_to_restock_point() -> None:
    fake_session = MagicMock()
    fake_item = ItemDB(id=1, name="Chicken", category_id=1, default_unit="lb", restock_point=Decimal("2"))
    fake_quantity_response = ItemQuantityResponse(name="Chicken", total_quantity=Decimal("2"), unit="lb")

    with (patch("src.domains.inventory.services.restock_item_service.get_item") as mock_get_item,
          patch("src.domains.inventory.services.restock_item_service.get_item_inventory_quantity") as mock_get_item_inventory_quantity):
        mock_get_item.return_value = fake_item
        mock_get_item_inventory_quantity.return_value = fake_quantity_response

        result = get_restock_status(session=fake_session, item_id=fake_item.id)

        assert result.needs_restock == True
        assert result.name == "Chicken"
        assert result.current_quantity == Decimal("2")
        assert result.restock_point == Decimal("2")
        assert result.unit == "lb"

def test_get_restock_status_returns_true_when_below_restock_point() -> None:
    fake_session = MagicMock()
    fake_item = ItemDB(id=1, name="Chicken", category_id=1, default_unit="lb", restock_point=Decimal("2"))
    fake_quantity_response = ItemQuantityResponse(name="Chicken", total_quantity=Decimal("1"), unit="lb")

    with (patch("src.domains.inventory.services.restock_item_service.get_item") as mock_get_item,
          patch("src.domains.inventory.services.restock_item_service.get_item_inventory_quantity") as mock_get_item_inventory_quantity):
        mock_get_item.return_value = fake_item
        mock_get_item_inventory_quantity.return_value = fake_quantity_response

        result = get_restock_status(session=fake_session, item_id=fake_item.id)

        assert result.needs_restock == True
        assert result.name == "Chicken"
        assert result.current_quantity == Decimal("1")
        assert result.restock_point == Decimal("2")
        assert result.unit == "lb"

def test_get_restock_status_returns_false_when_restock_point_is_none() -> None:
    fake_session = MagicMock()
    fake_item = ItemDB(id=1, name="Chicken", category_id=1, default_unit="lb", restock_point=None)
    fake_quantity_response = ItemQuantityResponse(name="Chicken", total_quantity=Decimal("1"), unit="lb")

    with (patch("src.domains.inventory.services.restock_item_service.get_item") as mock_get_item,
          patch("src.domains.inventory.services.restock_item_service.get_item_inventory_quantity") as mock_get_item_inventory_quantity):
        mock_get_item.return_value = fake_item
        mock_get_item_inventory_quantity.return_value = fake_quantity_response

        result = get_restock_status(session=fake_session, item_id=fake_item.id)

        assert result.needs_restock is False
        assert result.restock_point is None

def test_get_restock_status_rejects_missing_item() -> None:
        fake_session = MagicMock()

        with (patch("src.domains.inventory.services.restock_item_service.get_item") as mock_get_item):
            mock_get_item.return_value = None

            with pytest.raises(ValueError, match="Item does not exist."):
                get_restock_status(session=fake_session, item_id=1)



