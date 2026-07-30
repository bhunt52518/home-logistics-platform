from unittest.mock import patch

from fastapi.testclient import TestClient

from src.main import app
from src.domains.inventory.persistence.location_db import LocationDB


client = TestClient(app)


def test_post_location_returns_created_location() -> None:
    fake_location = LocationDB(
        id=1,
        household_id=1,
        name="Kitchen Refrigerator",
    )

    with patch(
        "src.api.routes.inventory.locations.create_inventory_location"
    ) as mock_create_location:
        mock_create_location.return_value = fake_location

        response = client.post(
            "/inventory/location",
            json={
                "household_id": 1,
                "name": "Kitchen Refrigerator",
            },
        )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "household_id": 1,
        "name": "Kitchen Refrigerator",
    }

    mock_create_location.assert_called_once()

    kwargs = mock_create_location.call_args.kwargs

    assert kwargs["household_id"] == 1
    assert kwargs["name"] == "Kitchen Refrigerator"
    assert "session" in kwargs


def test_post_location_rejects_blank_name() -> None:
    with patch(
        "src.api.routes.inventory.locations.create_inventory_location"
    ) as mock_create_location:
        response = client.post(
            "/inventory/location",
            json={
                "household_id": 1,
                "name": "   ",
            },
        )

    assert response.status_code == 422
    mock_create_location.assert_not_called()


def test_post_location_returns_400_when_household_does_not_exist() -> None:
    with patch(
        "src.api.routes.inventory.locations.create_inventory_location"
    ) as mock_create_location:
        mock_create_location.side_effect = ValueError(
            "Household does not exist."
        )

        response = client.post(
            "/inventory/location",
            json={
                "household_id": 999,
                "name": "Kitchen Refrigerator",
            },
        )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Household does not exist.",
    }

    mock_create_location.assert_called_once()