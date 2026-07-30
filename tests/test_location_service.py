from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from src.domains.inventory.persistence.household_db import HouseholdDB
from src.domains.inventory.persistence.location_db import LocationDB
from src.domains.inventory.services.location_service import (
    create_inventory_location,
)


def test_create_inventory_location_sends_validated_location_to_repository() -> None:
    fake_session = MagicMock()

    fake_household = HouseholdDB(
        id=1,
        name="Hunt Family",
    )

    fake_saved_location = LocationDB(
        id=1,
        household_id=1,
        name="Kitchen Refrigerator",
    )

    with (
        patch(
            "src.domains.inventory.services.location_service.get_household"
        ) as mock_get_household,
        patch(
            "src.domains.inventory.services.location_service.create_location"
        ) as mock_create_location,
    ):
        mock_get_household.return_value = fake_household
        mock_create_location.return_value = fake_saved_location

        result = create_inventory_location(
            session=fake_session,
            household_id=1,
            name="  Kitchen Refrigerator  ",
        )

        location_sent_to_repository = (
            mock_create_location.call_args.kwargs["location"]
        )

    mock_get_household.assert_called_once_with(
        session=fake_session,
        household_id=1,
    )

    assert location_sent_to_repository.household_id == 1
    assert location_sent_to_repository.name == "Kitchen Refrigerator"

    mock_create_location.assert_called_once_with(
        session=fake_session,
        location=location_sent_to_repository,
    )

    assert result == fake_saved_location


def test_create_inventory_location_rejects_missing_household() -> None:
    fake_session = MagicMock()

    with (
        patch(
            "src.domains.inventory.services.location_service.get_household"
        ) as mock_get_household,
        patch(
            "src.domains.inventory.services.location_service.create_location"
        ) as mock_create_location,
    ):
        mock_get_household.return_value = None

        with pytest.raises(
            ValueError,
            match="Household does not exist",
        ):
            create_inventory_location(
                session=fake_session,
                household_id=999,
                name="Kitchen Refrigerator",
            )

        mock_create_location.assert_not_called()


def test_create_inventory_location_rejects_blank_name() -> None:
    fake_session = MagicMock()
    fake_household = HouseholdDB(
        id=1,
        name="Hunt Family",
    )

    with (
        patch(
            "src.domains.inventory.services.location_service.get_household"
        ) as mock_get_household,
        patch(
            "src.domains.inventory.services.location_service.create_location"
        ) as mock_create_location,
    ):
        mock_get_household.return_value = fake_household

        with pytest.raises(ValidationError):
            create_inventory_location(
                session=fake_session,
                household_id=1,
                name="   ",
            )

        mock_create_location.assert_not_called()