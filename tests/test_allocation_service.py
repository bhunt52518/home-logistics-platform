from src.domains.inventory.models.inventory_allocation import InventoryAllocation
from src.domains.inventory.models.item_allocation_request import ItemAllocationRequest
from src.domains.inventory.services.allocation_service import is_allocation_valid

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