from src.database.base import Base
from src.domains.inventory.persistence.category_db import CategoryDB
from src.domains.inventory.persistence.household_db import HouseholdDB
from src.domains.inventory.persistence.inventory_record_db import InventoryRecordDB
from src.domains.inventory.persistence.item_db import ItemDB
from src.domains.inventory.persistence.location_db import LocationDB
from src.domains.inventory.repositories.inventory_repository import (
    create_household, create_category, create_location,create_item, create_inventory_record, get_category,
    get_items_with_restock_point
    )

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from datetime import date
from decimal import Decimal




def test_inventory_persistence_creates_expected_tables() -> None:
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(engine)

    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    assert set(table_names) == {
        "categories",
        "households",
        "inventory_records",
        "items",
        "locations",
    }

def test_household_can_be_saved_and_retrieved() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        household = HouseholdDB(name="Hunt Family")
        saved_household = create_household(session=session, household=household)
        retrieved_household = session.get(HouseholdDB,saved_household.id)

        assert saved_household is not None
        assert saved_household.id is not None
        assert saved_household.name == "Hunt Family"

        assert retrieved_household is not None
        assert retrieved_household.id == saved_household.id
        assert retrieved_household.name == "Hunt Family"

def test_location_can_be_save_and_retrieved() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    with Session(engine) as session:
        household = HouseholdDB(name="Hunt Family")
        saved_household = create_household(session=session, household=household)

        location = LocationDB(household_id=saved_household.id, name="Kitchen Refrigerator")
        saved_location = create_location(session=session, location=location)
        retrieved_location = session.get(LocationDB, saved_location.id)

        assert saved_location.id is not None
        assert saved_location.name == "Kitchen Refrigerator"
        assert saved_location.household_id == saved_household.id

        assert retrieved_location is not None
        assert retrieved_location.id is not None
        assert retrieved_location.name == "Kitchen Refrigerator"
        assert retrieved_location.household_id == saved_household.id

def test_category_can_be_saved_and_retrieved() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        category = CategoryDB(name="Meat", perishable_default=True)
        saved_category = create_category(session=session, category=category)
        retrieved_category = get_category(session=session, category_id=saved_category.id)

        assert saved_category.id is not None
        assert saved_category.name == "Meat"
        assert saved_category.perishable_default is True

        assert retrieved_category is not None
        assert retrieved_category.id is not None
        assert retrieved_category.name =="Meat"
        assert retrieved_category.perishable_default is True

def test_item_can_be_saved_and_retrieved() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        category = CategoryDB(name="meat", perishable_default=True)
        saved_category = create_category(session=session, category=category)

        
        item = ItemDB(name="Chicken", category_id=saved_category.id, default_unit="LB")
        saved_item = create_item(session=session, item=item)
        retrieved_item = session.get(ItemDB, saved_item.id)

        assert saved_item is not None
        assert saved_item.id is not None
        assert saved_item.name == "Chicken"

        assert retrieved_item is not None
        assert retrieved_item.id is not None
        assert retrieved_item.name =="Chicken"

def test_inventory_record_can_be_saved_and_retrieved() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        household = HouseholdDB(name="Hunt Family")
        saved_household = create_household(session=session, household=household)

        category = CategoryDB(name="Meat", perishable_default=True)
        saved_category = create_category(session=session, category=category)

        location = LocationDB(household_id=saved_household.id, name="Kitchen Refrigerator")
        saved_location = create_location(session=session, location=location)

        item = ItemDB(name="Chicken", category_id=saved_category.id, default_unit="LB")
        saved_item = create_item(session=session, item=item)

        inventory_record = InventoryRecordDB(item_id=saved_item.id, location_id=saved_location.id, quantity=Decimal("2"),
                                             unit=saved_item.default_unit, purchase_date=date(2025, 5, 27), expiration_date=None)
        saved_inventory_record = create_inventory_record(session=session, inventory_record=inventory_record)
        retrieved_inventory_record = session.get(InventoryRecordDB, saved_inventory_record.id)

        assert saved_inventory_record is not None
        assert saved_inventory_record.id is not None
        assert saved_inventory_record.quantity == Decimal("2")
        assert saved_inventory_record.purchase_date == date(2025, 5, 27)

        assert retrieved_inventory_record is not None
        assert retrieved_inventory_record.id is not None
        assert retrieved_inventory_record.quantity == Decimal("2")
        assert retrieved_inventory_record.item_id == saved_item.id
        assert retrieved_inventory_record.location_id == saved_location.id
        assert retrieved_inventory_record.unit == saved_item.default_unit
        assert retrieved_inventory_record.purchase_date == date(2025, 5, 27)
        assert retrieved_inventory_record.expiration_date is None

def test_get_items_with_restock_point_retrieves_items() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    item_1 = ItemDB(id=1, name="Chicken", category_id=1, default_unit="lb", restock_point=Decimal("2"))
    item_2 = ItemDB(id=2, name="Milk", category_id=2, default_unit="gal", restock_point=Decimal("1"))
    item_3 = ItemDB(id=3, name="Hammer", category_id=3, default_unit="each", restock_point=None)
    item_4 = ItemDB(id=4, name="AA Battery", category_id=3, default_unit="each", restock_point=Decimal("0"))
    item_5 = ItemDB(id=5, name="Steak", category_id=1, default_unit="lb", restock_point=Decimal("2"))

    items = [ item_1, item_2, item_3, item_4, item_5]

    with Session(engine) as session:
        session.add_all(items)
        session.commit()

        result = get_items_with_restock_point(session=session)

        result_ids =[item.id for item in result]

        assert len(result) == 4

        assert 1 in result_ids
        assert 2 in result_ids
        assert 4 in result_ids
        assert 5 in result_ids

        assert 3 not in result_ids

def test_get_items_with_restock_point_returns_empty_item_list() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    item_1 = ItemDB(id=1, name="Chicken", category_id=1, default_unit="lb", restock_point=None)
    item_2 = ItemDB(id=2, name="Milk", category_id=2, default_unit="gal", restock_point=None)
    item_3 = ItemDB(id=3, name="Hammer", category_id=3, default_unit="each", restock_point=None)

    items = [ item_1, item_2, item_3]

    with Session(engine) as session:
        session.add_all(items)
        session.commit()

        result = get_items_with_restock_point(session=session)

        assert result == []

        

