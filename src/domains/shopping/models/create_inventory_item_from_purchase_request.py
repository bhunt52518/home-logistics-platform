from pydantic import BaseModel, Field
from decimal import Decimal



class CreateInventoryItemFromPurchaseRequest(BaseModel):
    category_id: int
    restock_point: Decimal | None = Field(default=None, ge=Decimal("0"))
    target_stock: Decimal | None = Field(default=None, ge=Decimal("0"))

  