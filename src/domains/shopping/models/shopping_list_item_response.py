from pydantic import BaseModel, ConfigDict
from src.domains.shopping.models.shopping_list_source import ShoppingListSource

from decimal import Decimal




class ShoppingListItemResponse(BaseModel):
    id: int
    item_id: int | None
    name: str
    quantity: Decimal
    unit: str
    source: ShoppingListSource
    purchased: bool

    model_config = ConfigDict(from_attributes=True)
