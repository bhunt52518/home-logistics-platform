from decimal import Decimal
from datetime import date
from pydantic import BaseModel

class InventoryRecord(BaseModel):
    item_id: int
    location_id: int
    quantity: Decimal
    item_unit: str
    purchase_date: date
    expiration_date: date | None = None

