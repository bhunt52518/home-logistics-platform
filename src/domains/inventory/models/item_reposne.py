from pydantic import BaseModel, ConfigDict
from decimal import Decimal




class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category_id: int
    default_unit: str
    restock_point: Decimal | None
    target_stock: Decimal | None