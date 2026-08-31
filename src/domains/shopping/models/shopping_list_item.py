from decimal import Decimal
from pydantic import BaseModel, Field

from src.domains.shopping.models.shopping_list_source import ShoppingListSource




class ShoppingListItem (BaseModel):
    item_id: int | None = None
    name: str
    quantity: Decimal = Field(gt=Decimal("0"))
    unit: str
    source: ShoppingListSource
    purchased: bool = False