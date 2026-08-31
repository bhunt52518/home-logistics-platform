from src.database.base import Base
from src.domains.shopping.persistence.shopping_list_db import ShoppingListItemDB
from src.domains.shopping.models.shopping_list_item import ShoppingListItem
from src.domains.inventory.persistence.item_db import ItemDB
from src.domains.inventory.persistence.category_db import CategoryDB
from src.domains.shopping.models.shopping_list_source import ShoppingListSource
from src.domains.shopping.repositories.shopping_repository import (create_shopping_list_item, get_shopping_list_item,
                                                                   get_dulicate_shopping_list_item)

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from datetime import date
from decimal import Decimal




def test_shopping_list_persistence_creates_expected_table() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    assert set(table_names) == {"shopping_list_items", "categories", "items"}

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
        result = get_dulicate_shopping_list_item(session=session, shopping_list_db=new_item)

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
        result = get_dulicate_shopping_list_item(session=session, shopping_list_db=new_item)

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
        result = get_dulicate_shopping_list_item(session=session, shopping_list_db=new_item)

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
        result = get_dulicate_shopping_list_item(session=session, shopping_list_db=new_item)

        assert result is None
