from pydantic import BaseModel, field_validator, Field
from src.core.services.name_validator import NameValidator
from decimal import Decimal





class ItemCreate(BaseModel):

    name: str
    category_id: int
    default_unit: str
    restock_point: Decimal | None = Field(default=None, ge=Decimal("0"))

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return NameValidator.validate_non_empty(value)

    




    