from unittest.mock import MagicMock, patch

from src.domains.inventory.persistence.category_db import CategoryDB
from src.domains.inventory.services.category_service import (
    create_inventory_category,
)


def test_create_inventory_category_sends_validated_category_to_repository() -> None:
    fake_session = MagicMock()

    fake_saved_category = CategoryDB(
        id=1,
        name="Meat",
        perishable_default=True,
    )

    with patch(
        "src.domains.inventory.services.category_service.create_category"
    ) as mock_create_category:
        mock_create_category.return_value = fake_saved_category

        result = create_inventory_category(
            session=fake_session,
            name="  Meat  ",
            perishable_default=True,
        )

        category_sent_to_repository = (
            mock_create_category.call_args.kwargs["category"]
        )

    assert category_sent_to_repository.name == "Meat"
    assert category_sent_to_repository.perishable_default is True

    mock_create_category.assert_called_once_with(
        session=fake_session,
        category=category_sent_to_repository,
    )

    assert result == fake_saved_category