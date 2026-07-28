from src.domains.inventory.models.household_create import HouseholdCreate

from pydantic import ValidationError

import pytest




def test_household_create_accepts_valid_name() -> None:
    request_body = {"name": "Hunt Family"}

    household = HouseholdCreate(**request_body)

    assert household.name == "Hunt Family"

def test_household_create_rejects_invalid_name() -> None:
    with pytest.raises(ValidationError):
        HouseholdCreate(name="  ")