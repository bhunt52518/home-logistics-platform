from src.domains.inventory.models.inventory_allocation import InventoryAllocation
from src.domains.inventory.models.item_allocation_request import ItemAllocationRequest
from src.domains.inventory.services.allocation_service import (is_allocation_valid, create_inventory_records, process_allocation)
from src.domains.inventory.persistence.inventory_record_db import InventoryRecordDB

from unittest.mock import MagicMock
from unittest.mock import patch

from datetime import date
from decimal import Decimal 

import pytest

def test_is_allocation_valid_is_true():

    refrigerator = InventoryAllocation(location_id=1, quantity=Decimal("2"))
    freezer = InventoryAllocation(location_id=2, quantity=Decimal("8"))

    allocation_request = ItemAllocationRequest(item_id= 37, purchased_quantity=Decimal("10"), item_unit= "lb", allocations= [refrigerator, freezer])

    result = is_allocation_valid(allocation_request)

    assert result is True

def test_is_allocation_valid_is_false():

    refrigerator = InventoryAllocation(location_id=1, quantity=Decimal("2"))
    freezer = InventoryAllocation(location_id=2, quantity=Decimal("7"))

    allocation_request = ItemAllocationRequest(item_id= 37, purchased_quantity=Decimal("10"), item_unit= "lb", allocations= [refrigerator, freezer])

    result = is_allocation_valid(allocation_request)

    assert result is False

def test_create_inventory_records_returns_record_for_each_allocation() -> None:

    refrigerator = InventoryAllocation(location_id=1, quantity=Decimal("2"))
    freezer = InventoryAllocation(location_id=2, quantity=Decimal("8"))

    allocation_request = ItemAllocationRequest(item_id= 37, purchased_quantity=Decimal("10"), item_unit= "lb", allocations= [refrigerator, freezer])

    records = create_inventory_records(allocation_request)

    assert len(records) == 2

    assert records[0].item_id == allocation_request.item_id
    assert records[0].location_id == refrigerator.location_id
    assert records[0].quantity == refrigerator.quantity
    assert records[0].unit == allocation_request.item_unit
    assert records[0].purchase_date == date.today()
    assert records[0].expiration_date is None

    assert records[1].item_id == allocation_request.item_id
    assert records[1].location_id == freezer.location_id
    assert records[1].quantity == freezer.quantity
    assert records[1].unit == allocation_request.item_unit
    assert records[1].purchase_date == date.today()
    assert records[1].expiration_date is None

def test_process_allocation_sends_record_for_each_allocation() -> None:
    fake_saved_records = [InventoryRecordDB(id=1,item_id=1, location_id=1, quantity=Decimal("2"), unit="lb", purchase_date=date.today(), expiration_date=None),
                          InventoryRecordDB(id=2,item_id=1, location_id=2, quantity=Decimal("3"), unit="lb", purchase_date=date.today(), expiration_date=None)] 
    refrigerator = InventoryAllocation(location_id=1, quantity=Decimal(2))
    freezer = InventoryAllocation(location_id=2, quantity=Decimal("3"))
    allocation_request = ItemAllocationRequest(item_id=1, purchased_quantity=Decimal("5"), item_unit="lb", allocations=[refrigerator, freezer])

    fake_session = MagicMock()


    with patch("src.domains.inventory.services.allocation_service.apply_allocations") as mock_apply_allocation:
        mock_apply_allocation.return_value = fake_saved_records

        result = process_allocation(session=fake_session, allocation_request=allocation_request) 

        saved_records = mock_apply_allocation.call_args.kwargs["inventory_records"]

        assert len(saved_records) == 2

        assert saved_records[0].item_id == allocation_request.item_id
        assert saved_records[0].location_id == refrigerator.location_id
        assert saved_records[0].quantity == refrigerator.quantity
        assert saved_records[0].unit == allocation_request.item_unit

        assert saved_records[1].item_id == allocation_request.item_id
        assert saved_records[1].location_id == freezer.location_id
        assert saved_records[1].quantity == freezer.quantity
        assert saved_records[1].unit == allocation_request.item_unit

        mock_apply_allocation.assert_called_once_with(session=fake_session, inventory_records=saved_records)

        assert result == fake_saved_records

def test_process_allocation_sends_record_for_each_allocation() -> None:
    refrigerator = InventoryAllocation(location_id=1, quantity=Decimal(2))
    freezer = InventoryAllocation(location_id=2, quantity=Decimal("3"))
    allocation_request = ItemAllocationRequest(item_id=1, purchased_quantity=Decimal("10"), item_unit="lb", allocations=[refrigerator, freezer])

    fake_session = MagicMock()


    with patch("src.domains.inventory.services.allocation_service.apply_allocations") as mock_apply_allocation:
        with pytest.raises(ValueError, match="Allocation quantity does not equal purchased quantity."):
            process_allocation(session=fake_session, allocation_request=allocation_request)

        mock_apply_allocation.assert_not_called