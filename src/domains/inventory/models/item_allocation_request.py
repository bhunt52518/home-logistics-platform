from src.domains.inventory.models.inventory_allocation import InventoryAllocation

from pydantic import BaseModel, Field
from decimal import Decimal


class ItemAllocationRequest(BaseModel):

    item_id: int
    purchased_quantity: Decimal = Field(gt=0)
    item_unit: str
    allocations: list[InventoryAllocation]
    


