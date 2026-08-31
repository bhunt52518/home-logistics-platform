from decimal import Decimal
from pydantic import BaseModel, Field




class ShoppingListMergeSuggestion(BaseModel):
    shopping_list_item_id: int
    existing_quantity: Decimal = Field(gt=Decimal("0"))
    requested_quantity: Decimal = Field(gt=Decimal("0"))
    merged_quantity: Decimal = Field(gt=Decimal("0"))
    name: str
    unit: str
