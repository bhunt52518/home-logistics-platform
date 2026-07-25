from src.domains.inventory.models.inventory_allocation import InventoryAllocation
from src.domains.inventory.models.item_allocation_request import ItemAllocationRequest
from src.domains.inventory.services.allocation_service import (is_allocation_valid, create_inventory_records)

from datetime import date

from decimal import Decimal 

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
    assert records[0].item_unit == allocation_request.item_unit
    assert records[0].purchase_date == date.today()
    assert records[0].expiration_date is None

    assert records[1].item_id == allocation_request.item_id
    assert records[1].location_id == freezer.location_id
    assert records[1].quantity == freezer.quantity
    assert records[1].item_unit == allocation_request.item_unit
    assert records[1].purchase_date == date.today()
    assert records[1].expiration_date is None