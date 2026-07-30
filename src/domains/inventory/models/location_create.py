from pydantic import BaseModel, field_validator
from src.core.services.name_validator import NameValidator

class LocationCreate(BaseModel):
    household_id: int
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return NameValidator.validate_non_empty(value)