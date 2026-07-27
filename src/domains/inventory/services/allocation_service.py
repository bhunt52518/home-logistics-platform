from sqlalchemy.orm import Session

from src.domains.inventory.models.item_allocation_request import ItemAllocationRequest
from src.domains.inventory.models.inventory_record import InventoryRecord
from src.domains.inventory.persistence.inventory_record_db import InventoryRecordDB
from src.domains.inventory.repositories.inventory_repository import apply_allocations

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
        inventory_record = InventoryRecord(item_id = allocation_request.item_id, unit = allocation_request.item_unit, location_id = allocation.location_id,
                                           quantity = allocation.quantity, purchase_date = date.today(), expiration_date = None)
        inventory_records.append(inventory_record)

    return inventory_records

def process_allocation(session: Session, allocation_request: ItemAllocationRequest) -> list[InventoryRecordDB]:

    if not is_allocation_valid(allocation_request):
        raise ValueError("Allocation quantity does not equal purchased quantity.")

    inventory_records = create_inventory_records(allocation_request)

    return apply_allocations(session=session, inventory_records=inventory_records)
