from decimal import Decimal

from pydantic import BaseModel, ConfigDict




class ItemQuantityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    total_quantity: Decimal
    unit: str