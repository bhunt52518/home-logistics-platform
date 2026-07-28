from pydantic import BaseModel, field_validator




class HouseholdCreate(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned_name = value.strip()

        if not cleaned_name:
            raise ValueError("Household name cannot be empty.")

        return cleaned_name