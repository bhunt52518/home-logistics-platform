from src.domains.inventory.services.restock_item_service import get_restock_status, get_items_needing_restock
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

def test_get_items_needing_restocked() -> None:
    fake_session = MagicMock()

    fake_item_1 = ItemDB(id=1, name="Chicken", category_id=1, default_unit="lb", restock_point=Decimal("2"))
    fake_item_2 = ItemDB(id=2, name="Milk", category_id=2, default_unit="gal", restock_point=None)
    fake_item_3 = ItemDB(id=3, name="Steak", category_id=1, default_unit="lb", restock_point=Decimal("1"))
    fake_item_4 = ItemDB(id=4, name="Oatmeal", category_id=3, default_unit="box", restock_point=Decimal("0"))

    fake_restock_response_1 = RestockStatusResponse(name="Chicken",current_quantity=Decimal("1"), restock_point=Decimal("2"), unit="lb", needs_restock=True)
    fake_restock_response_2 = RestockStatusResponse(name="Milk",current_quantity=Decimal("1"), restock_point=None, unit="gal", needs_restock=False)
    fake_restock_response_3 = RestockStatusResponse(name="Steak",current_quantity=Decimal("2"), restock_point=Decimal("1"), unit="lb", needs_restock=False)
    fake_restock_response_4 = RestockStatusResponse(name="Oatmeal",current_quantity=Decimal("0"), restock_point=Decimal("0"), unit="lb", needs_restock=True)
    
    fake_items = [fake_item_1, fake_item_2, fake_item_3, fake_item_4]

    with (patch("src.domains.inventory.services.restock_item_service.get_items_with_restock_point") as mock_get_items_with_restock_point,
          patch("src.domains.inventory.services.restock_item_service.get_restock_status") as mock_get_restock_status):
        mock_get_items_with_restock_point.return_value = fake_items
        mock_get_restock_status.side_effect = [fake_restock_response_1, fake_restock_response_2, fake_restock_response_3, fake_restock_response_4]

        result = get_items_needing_restock(session=fake_session)
        result_names = [item.name for item in result]

        assert len(result) == 2

        assert "Chicken" in result_names
        assert "Oatmeal" in result_names

        assert "Milk" not in result_names
        assert "Steak" not in result_names

def test_get_items_needing_restocked_returns_empty_list() -> None:
    fake_session = MagicMock()

    fake_item_1 = ItemDB(id=1, name="Chicken", category_id=1, default_unit="lb", restock_point=Decimal("2"))
    fake_item_2 = ItemDB(id=2, name="Milk", category_id=2, default_unit="gal", restock_point=None)
    fake_item_3 = ItemDB(id=3, name="Steak", category_id=1, default_unit="lb", restock_point=Decimal("1"))
    fake_item_4 = ItemDB(id=4, name="Oatmeal", category_id=3, default_unit="box", restock_point=Decimal("0"))

    fake_restock_response_1 = RestockStatusResponse(name="Chicken",current_quantity=Decimal("6"), restock_point=Decimal("2"), unit="lb", needs_restock=False)
    fake_restock_response_2 = RestockStatusResponse(name="Milk",current_quantity=Decimal("1"), restock_point=None, unit="gal", needs_restock=False)
    fake_restock_response_3 = RestockStatusResponse(name="Steak",current_quantity=Decimal("2"), restock_point=Decimal("1"), unit="lb", needs_restock=False)
    fake_restock_response_4 = RestockStatusResponse(name="Oatmeal",current_quantity=Decimal("1"), restock_point=Decimal("0"), unit="lb", needs_restock=False)
    
    fake_items = [fake_item_1, fake_item_2, fake_item_3, fake_item_4]

    with (patch("src.domains.inventory.services.restock_item_service.get_items_with_restock_point") as mock_get_items_with_restock_point,
          patch("src.domains.inventory.services.restock_item_service.get_restock_status") as mock_get_restock_status):
        mock_get_items_with_restock_point.return_value = fake_items
        mock_get_restock_status.side_effect = [fake_restock_response_1, fake_restock_response_2, fake_restock_response_3, fake_restock_response_4]

        result = get_items_needing_restock(session=fake_session)

        assert result == []
def test_get_items_needing_restock_does_not_check_status_when_no_items() -> None:
    fake_session = MagicMock()

    with (patch("src.domains.inventory.services.restock_item_service.get_items_with_restock_point") as mock_get_items_with_restock_point,
          patch("src.domains.inventory.services.restock_item_service.get_restock_status") as mock_get_restock_status):
        mock_get_items_with_restock_point.return_value = []

        result = get_items_needing_restock(session=fake_session)

        assert result == []
        mock_get_restock_status.assert_not_called()
                



