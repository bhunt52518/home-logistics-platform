from pydantic import BaseModel
from decimal import Decimal


class InventoryAllocation(BaseModel):

    quantity: Decimal
    location_id: int
