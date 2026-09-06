from src.database.base import Base
from src.domains.shopping.persistence.shopping_list_db import ShoppingListItemDB
from src.domains.shopping.models.shopping_list_item import ShoppingListItem
from src.domains.inventory.persistence.item_db import ItemDB
from src.domains.inventory.persistence.category_db import CategoryDB
from src.domains.inventory.persistence.household_db import HouseholdDB
from src.domains.inventory.persistence.inventory_record_db import InventoryRecordDB
from src.domains.inventory.persistence.location_db import LocationDB
from src.domains.shopping.models.shopping_list_source import ShoppingListSource
from src.domains.shopping.repositories.shopping_repository import (
    create_shopping_list_item, get_shopping_list_item,get_duplicate_shopping_list_item, update_shopping_list_quantity,
    get_active_shopping_list_items, update_shopping_list_item_as_purchased)

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from datetime import date
from decimal import Decimal

import pytest




def test_shopping_list_persistence_creates_expected_table() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    assert set(table_names) == {"shopping_list_items", "categories", "items", "households", "inventory_records", "locations"}

def test_shopping_list_can_be_saved_and_retrieved() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session: 
        shopping_list_item = ShoppingListItemDB(
            name="Birthday Candles", quantity=Decimal("1"), unit="pack", source=ShoppingListSource.MANUAL,
            item_id=None, purchased=False
        )
        saved_shopping_list = create_shopping_list_item(session=session, shopping_list=shopping_list_item)
        retrieved_shopping_list = get_shopping_list_item(session=session, shopping_list_id=saved_shopping_list.id)

        assert saved_shopping_list.id is not None
        assert saved_shopping_list.name == "Birthday Candles"
        assert saved_shopping_list.quantity == Decimal("1")
        assert saved_shopping_list.unit == "pack"
        assert saved_shopping_list.source == ShoppingListSource.MANUAL
        assert saved_shopping_list.item_id is None
        assert saved_shopping_list.purchased is False

        assert retrieved_shopping_list.id is not None
        assert retrieved_shopping_list.name == "Birthday Candles"
        assert retrieved_shopping_list.quantity == Decimal("1")
        assert retrieved_shopping_list.unit == "pack"
        assert retrieved_shopping_list.source == ShoppingListSource.MANUAL
        assert retrieved_shopping_list.item_id is None
        assert retrieved_shopping_list.purchased is False

def test_shopping_list_returns_duplicate_entry() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        existing_item = ShoppingListItem(
            name="Chicken", quantity=Decimal("2"), unit="lb", source=ShoppingListSource.RESTOCK,
            item_id=1
        )
        new_item = ShoppingListItemDB(
            name="Chicken", quantity=Decimal("3"), unit="lb", source=ShoppingListSource.RESTOCK,
            item_id=1, purchased=False
        )

        saved_item = create_shopping_list_item(session=session, shopping_list=existing_item)
        result = get_duplicate_shopping_list_item(session=session, shopping_list_db=new_item)

        assert result is not None
        assert result.id == saved_item.id
        assert result.item_id == 1

def test_shopping_list_returns_duplicate_entry_without_item_id() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        existing_item = ShoppingListItem(
            name="chicken", quantity=Decimal("2"), unit="lb", source=ShoppingListSource.RESTOCK,
            item_id=1
        )
        new_item = ShoppingListItemDB(
            name="Chicken", quantity=Decimal("3"), unit="lb ", source=ShoppingListSource.MANUAL,
            item_id=None, purchased=False
        )

        saved_item = create_shopping_list_item(session=session, shopping_list=existing_item)
        result = get_duplicate_shopping_list_item(session=session, shopping_list_db=new_item)

        assert result is not None
        assert result.name == "chicken"
        assert result.name == saved_item.name

def test_shopping_list_returns_none() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        existing_item = ShoppingListItem(
            name="chicken", quantity=Decimal("2"), unit="lb", source=ShoppingListSource.RESTOCK,
            item_id=1
        )
        new_item = ShoppingListItemDB(
            name="Steak", quantity=Decimal("3"), unit="lb", source=ShoppingListSource.MANUAL,
            item_id=2, purchased=False
        )

        saved_item = create_shopping_list_item(session=session, shopping_list=existing_item)
        result = get_duplicate_shopping_list_item(session=session, shopping_list_db=new_item)

        assert result is None

def test_shopping_list_returns_none_when_purchased_true() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        existing_item = ShoppingListItem(
            name="chicken", quantity=Decimal("2"), unit="lb", source=ShoppingListSource.RESTOCK,
            item_id=1, purchased=True
        )
        new_item = ShoppingListItemDB(
            name="Chicken", quantity=Decimal("3"), unit="lb", source=ShoppingListSource.MANUAL,
            item_id=1, purchased=False
        )

        saved_item = create_shopping_list_item(session=session, shopping_list=existing_item)
        result = get_duplicate_shopping_list_item(session=session, shopping_list_db=new_item)

        assert result is None

def test_update_shopping_list_quantity() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        existing_list = ShoppingListItemDB(
            name="Chicken", quantity=Decimal("2"), unit="lb", source=ShoppingListSource.RESTOCK,
            item_id=1, purchased=False
        )

        session.add(existing_list)
        session.commit()
        session.refresh(existing_list)

        result = update_shopping_list_quantity(session=session, shopping_list=existing_list, quantity=Decimal("5"))

        assert result.name == "Chicken"
        assert result.quantity == Decimal("5")
        assert result.unit == "lb"
        assert result.source == ShoppingListSource.RESTOCK
        assert result.item_id == 1
        assert result.purchased == False

def test_get_active_shopping_list_items_returns_valid_list() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        item_1 = ShoppingListItemDB(
            id=1, item_id=1, name="Chicken", quantity=Decimal("3"), unit="lb",
            source=ShoppingListSource.RESTOCK, purchased=False)
        item_2 = ShoppingListItemDB(
            id=2, item_id=2, name="Milk", quantity=Decimal("2"), unit="gal",
            source=ShoppingListSource.RESTOCK, purchased=False)
        item_3 = ShoppingListItemDB(
            id=4, item_id=4, name="Candles", quantity=Decimal("3"), unit="lb",
            source=ShoppingListSource.RESTOCK, purchased=True)
        items_db = [item_1, item_2, item_3]

        session.add_all(items_db)
        session.commit()


        result = get_active_shopping_list_items(session=session)
        result_names = [item.name for item in result]

        assert len(result) == 2
        assert "Chicken" in result_names
        assert "Milk" in result_names

def test_update_shopping_list_item_as_purchased() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        fake_shopping_list_item_db = ShoppingListItemDB(
            id=1, item_id=1, name="Chicken", quantity=Decimal("3"), unit="lb",
            source=ShoppingListSource.RESTOCK, purchased=False
        )

        session.add(fake_shopping_list_item_db)
        session.commit()
        session.refresh(fake_shopping_list_item_db)

        result = update_shopping_list_item_as_purchased(
            session=session, shopping_list_item_id=fake_shopping_list_item_db.item_id, purchased=True)
        saved_item = get_shopping_list_item(session=session, shopping_list_id=fake_shopping_list_item_db.id)

        assert result.name == "Chicken"
        assert result.item_id == 1
        assert result.quantity == Decimal("3")
        assert result.unit == "lb"
        assert result.source == ShoppingListSource.RESTOCK
        assert result.purchased == True

        assert saved_item is not None
        assert saved_item.purchased is True

def test_update_shopping_list_item_as_purchased_returns_error() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        with pytest.raises(ValueError, match="Shopping list item does not exist."):
            update_shopping_list_item_as_purchased(
                session=session, shopping_list_item_id=999, purchased=True)


