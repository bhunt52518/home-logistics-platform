from src.domains.inventory.models.item_allocation_request import ItemAllocationRequest
from src.domains.inventory.models.inventory_record import InventoryRecord

from decimal import Decimal
from datetime import date



def is_allocation_valid(allocation_request: ItemAllocationRequest) -> bool:

    allocated_total = Decimal("0")

    for allocation in allocation_request.allocations:
        allocated_total += allocation.quantity

    return (allocated_total == allocation_request.purchased_quantity)

def create_inventory_records(allocation_request: ItemAllocationRequest) -> list[InventoryRecord]:

    inventory_records: list[InventoryRecord] = []

    # Will need to change purchase date later and add expiration date

    for allocation in allocation_request.allocations:
        inventory_record = InventoryRecord(item_id = allocation_request.item_id, item_unit = allocation_request.item_unit, location_id = allocation.location_id,
                                           quantity = allocation.quantity, purchase_date = date.today(), expiration_date = None)
        inventory_records.append(inventory_record)

    return inventory_records
