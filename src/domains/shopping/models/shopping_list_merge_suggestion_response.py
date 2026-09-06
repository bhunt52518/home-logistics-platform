from pydantic import BaseModel

from decimal import Decimal




class ShoppingListMergeSuggestionResponse(BaseModel):
    shopping_list_item_id: int
    existing_quantity: Decimal
    requested_quantity: Decimal
    merged_quantity: Decimal
    name: str
    unit: str