from unittest.mock import patch

from fastapi.testclient import TestClient

from src.main import app
from src.domains.inventory.persistence.household_db import HouseholdDB


client = TestClient(app)


def test_post_household_returns_created_household() -> None:
    fake_household = HouseholdDB(
        id=1,
        name="Hunt Family",
    )

    with patch(
        "src.api.routes.inventory.households.create_inventory_household"
    ) as mock_create_household:
        mock_create_household.return_value = fake_household

        response = client.post(
            "/inventory/households",
            json={"name": "Hunt Family"},
        )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Hunt Family",
    }

    mock_create_household.assert_called_once()

def test_post_household_rejects_blank_name() -> None:
    with patch(
        "src.api.routes.inventory.households.create_inventory_household"
    ) as mock_create_household:
        response = client.post(
            "/inventory/households",
            json={"name": "   "},
        )

    assert response.status_code == 422
    mock_create_household.assert_not_called()