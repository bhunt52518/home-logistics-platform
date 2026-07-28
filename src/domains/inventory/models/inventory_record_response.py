from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class InventoryRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item_id: int
    location_id: int
    quantity: Decimal
    unit: str
    purchase_date: date
    expiration_date: date | None