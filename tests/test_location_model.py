from src.domains.inventory.models.location_create import LocationCreate

from pydantic import ValidationError

import pytest




def test_location_create_accepts_valid_name() -> None:
    request_body = {"household_id": 1, "name": "Freezer"}

    location = LocationCreate(**request_body)

    assert location.household_id == 1
    assert location.name == "Freezer"

def test_category_create_rejects_invalid_name() -> None:
    with pytest.raises(ValidationError):
        LocationCreate(name="  ")