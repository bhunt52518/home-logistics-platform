from pydantic import BaseModel, Field
from decimal import Decimal


class InventoryAllocation(BaseModel):

    location_id: int
    quantity: Decimal = Field(gt=0)
