from src.domains.inventory.models.inventory_allocation import InventoryAllocation

from pydantic import BaseModel





class StockPurchasedItemRequest(BaseModel):
    allocations: list[InventoryAllocation]