from src.database.base import Base
from src.domains.inventory.persistence.category_db import CategoryDB
from src.domains.inventory.persistence.household_db import HouseholdDB
from src.domains.inventory.persistence.inventory_record_db import InventoryRecordDB
from src.domains.inventory.persistence.item_db import ItemDB
from src.domains.inventory.persistence.location_db import LocationDB

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

    session.add(household)
    session.commit()

    saved_household = session.get(HouseholdDB, household.id)

    assert saved_household is not None
    assert saved_household.id == household.id
    assert saved_household.name == "Hunt Family"