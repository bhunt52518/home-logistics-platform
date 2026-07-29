from unittest.mock import patch

from fastapi.testclient import TestClient

from src.main import app
from src.domains.inventory.persistence.category_db import CategoryDB


client = TestClient(app)


def test_post_category_return_created_category() -> None:
    fake_category = CategoryDB(id=1, name="Meat", perishable_default=True)

    with patch("src.api.routes.inventory.category.create_inventory_category") as mock_create_category:
        mock_create_category.return_value = fake_category

        response = client.post("/inventory/category", json={"name": "Meat", "perishable_default": True})

        assert response.status_code == 201
        assert response.json() == {"id": 1, "name": "Meat", "perishable_default": True}

        mock_create_category.assert_called_once()

        kwargs = mock_create_category.call_args.kwargs

        assert kwargs["name"] == "Meat"
        assert kwargs["perishable_default"] is True

def test_post_category_rejects_blank_name() -> None:

    with patch("src.api.routes.inventory.category.create_inventory_category") as mock_create_category:
        response = client.post("inventory/category", json={"name": "   ", "perishable_default": True})


        assert response.status_code == 422
        mock_create_category.assert_not_called()