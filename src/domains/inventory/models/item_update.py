from pydantic import BaseModel, Field, field_validator
from src.core.services.name_validator import NameValidator
from decimal import Decimal




class ItemUpdate(BaseModel):
    name: str | None = None
    category_id: int | None = None
    default_unit: str | None = None
    restock_point: Decimal | None = Field(default=None, ge=Decimal("0"))
    target_stock: Decimal | None = Field(default=None, ge=Decimal("0"))

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value == None:
            return None
        else:
            return NameValidator.validate_non_empty(value)