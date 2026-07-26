from src.database.base import Base
from src.domains.inventory.persistence.category_db import CategoryDB
from src.domains.inventory.persistence.household_db import HouseholdDB
from src.domains.inventory.persistence.inventory_record_db import InventoryRecordDB
from src.domains.inventory.persistence.item_db import ItemDB
from src.domains.inventory.persistence.location_db import LocationDB
from src.domains.inventory.repositories.inventory_repository import (create_household, create_category, create_location)

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session




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
        retrieved_category = session.get(CategoryDB, saved_category.id)

        assert saved_category.id is not None
        assert saved_category.name == "Meat"
        assert saved_category.perishable_default is True

        assert retrieved_category is not None
        assert retrieved_category.id is not None
        assert retrieved_category.name =="Meat"
        assert retrieved_category.perishable_default is True
