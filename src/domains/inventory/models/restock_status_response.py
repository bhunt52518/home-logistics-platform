from pydantic import BaseModel, ConfigDict
from decimal import Decimal





class RestockStatusResponse(BaseModel):
    name: str
    current_quantity: Decimal
    restock_point: Decimal | None
    unit: str
    needs_restock: bool
    target_stock: Decimal | None
    suggested_purchase_quantity: Decimal | None