from src.domains.inventory.models.inventory_allocation import InventoryAllocation

from pydantic import BaseModel
from decimal import Decimal


class ItemAllocationRequest(BaseModel):

    item_id: int
    purchased_quantity: Decimal
    item_unit: str
    allocations: list[InventoryAllocation]
    


