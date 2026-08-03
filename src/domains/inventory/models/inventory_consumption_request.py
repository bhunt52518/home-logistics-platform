from src.core.services.quantity_validator import QuantityValidator
from decimal import Decimal

from pydantic import BaseModel, field_validator





class InventoryConsumptionRequest(BaseModel):
    inventory_record_id: int
    quantity: Decimal

    @field_validator("quantity")
    @classmethod
    def validate_greater_than_zero(cls, value: Decimal) -> Decimal:
        return QuantityValidator.validate_greater_than_zero(value)