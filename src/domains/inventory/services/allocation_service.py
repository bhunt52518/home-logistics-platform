from src.domains.inventory.models.item_allocation_request import ItemAllocationRequest

from decimal import Decimal



def is_allocation_valid(allocation_request: ItemAllocationRequest) -> bool:

    allocated_total = Decimal("0")

    for allocation in allocation_request.allocations:
        allocated_total += allocation.quantity

    return (allocated_total == allocation_request.purchased_quantity)
