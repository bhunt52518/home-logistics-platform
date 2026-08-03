from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from src.domains.inventory.persistence.inventory_record_db import InventoryRecordDB
from src.domains.inventory.models.inventory_consumption_request import InventoryConsumptionRequest
from src.domains.inventory.services.inventory_consumption_service import consume_inventory

from datetime import date





def test_inventory_consumption_updates_inventory_quantity() -> None:
    fake_session = MagicMock()
    fake_saved_inventory_record = InventoryRecordDB(id=1, item_id=1, location_id=1, quantity=10, unit="lb", purchase_date=date(2026,5,26), expiration_date=None)
    fake_consumption_request = InventoryConsumptionRequest(inventory_record_id=1, quantity=3)

    with (patch("src.domains.inventory.services.inventory_consumption_service.get_inventory_record") as mock_get_inventory_record,
          patch("src.domains.inventory.services.inventory_consumption_service.update_inventory_record") as mock_update_inventory_record):
        mock_get_inventory_record.return_value = fake_saved_inventory_record
        mock_update_inventory_record.return_value = fake_saved_inventory_record

        result = consume_inventory(session=fake_session, consumption_request=fake_consumption_request)

        assert result.quantity == 7
        assert result.id == 1
        mock_update_inventory_record.assert_called_once()

def test_inventory_consumption_rejects_quantity_greater_than_available() -> None:
    fake_session = MagicMock()
    fake_saved_inventory_record = InventoryRecordDB(id=1, item_id=1, location_id=1, quantity=2, unit="lb", purchase_date=date(2026,5,26), expiration_date=None)
    fake_consumption_request = InventoryConsumptionRequest(inventory_record_id=1, quantity=5)

    with (patch("src.domains.inventory.services.inventory_consumption_service.get_inventory_record") as mock_get_inventory_record,
          patch("src.domains.inventory.services.inventory_consumption_service.update_inventory_record") as mock_update_inventory_record):
        mock_get_inventory_record.return_value = fake_saved_inventory_record

        with pytest.raises(ValueError, match="Consumption amount can not exceed inventory quantity"):
            consume_inventory(session=fake_session, consumption_request=fake_consumption_request)

        mock_update_inventory_record.assert_not_called()

def test_inventory_consumption_rejects_missing_record() -> None:
    fake_session = MagicMock()
    fake_consumption_request = InventoryConsumptionRequest(inventory_record_id=1, quantity=5)

    with (patch("src.domains.inventory.services.inventory_consumption_service.get_inventory_record") as mock_get_inventory_record,
          patch("src.domains.inventory.services.inventory_consumption_service.update_inventory_record") as mock_update_inventory_record):
        mock_get_inventory_record.return_value = None

        with pytest.raises(ValueError, match="Record does not exist."):
            consume_inventory(session=fake_session, consumption_request=fake_consumption_request)

        mock_update_inventory_record.assert_not_called()