from pydantic import BaseModel, field_validator, model_validator, Field
from src.core.services.name_validator import NameValidator
from src.core.services.target_stock_validator import TargetStockValidator
from decimal import Decimal





class ItemCreate(BaseModel):

    name: str
    category_id: int
    default_unit: str
    restock_point: Decimal | None = Field(default=None, ge=Decimal("0"))
    target_stock: Decimal | None = Field(default=None, ge=Decimal("0"))

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return NameValidator.validate_non_empty(value)

    @model_validator(mode="after")
    def validate_target_stock(self) -> "ItemCreate":
        TargetStockValidator.validate_target_stock_not_less_than_restock_point(self.restock_point, self.target_stock)

        return self
        

    




    