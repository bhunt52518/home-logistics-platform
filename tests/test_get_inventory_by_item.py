from src.database.base import Base
from src.domains.inventory.persistence.category_db import CategoryDB
from src.domains.inventory.persistence.household_db import HouseholdDB
from src.domains.inventory.persistence.inventory_record_db import InventoryRecordDB
from src.domains.inventory.persistence.item_db import ItemDB
from src.domains.inventory.persistence.location_db import LocationDB
from src.domains.inventory.repositories.inventory_repository import (create_household, create_category, create_location,
                                                                     create_item, create_inventory_record, get_category, get_inventory_record_by_item)

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from datetime import date
from decimal import Decimal




def test_get_inventory_records_by_item_returns_only_matching_records() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        household = HouseholdDB(name="Hunt Family")
        saved_household = create_household(session=session, household=household)

        location = LocationDB(household_id=saved_household.id, name="Kitchen")
        saved_location = create_location(session=session, location=location)

        category = CategoryDB(name="Meat", perishable_default=True)
        saved_category = create_category(session=session, category=category)

        chicken_item = ItemDB(name="chicken", category_id=saved_category.id, default_unit="lb")
        saved_chicken_item = create_item(session=session, item=chicken_item)

        steak_item = ItemDB(name="Steak", category_id=saved_category.id, default_unit="lb")
        saved_steak_item = create_item(session=session, item=steak_item)

        chicken_record_1 = InventoryRecordDB(item_id=saved_chicken_item.id, location_id=saved_location.id, quantity=2,
                                             unit=saved_chicken_item.default_unit, purchase_date=date(2026,8,4), expiration_date=date(2026,8,10))
        saved_chicken_record_1 = create_inventory_record(session=session, inventory_record=chicken_record_1)

        chicken_record_2 = InventoryRecordDB(item_id=saved_chicken_item.id, location_id=saved_location.id, quantity=3,
                                             unit=saved_chicken_item.default_unit, purchase_date=date(2026,8,6), expiration_date=date(2026,8,10))
        saved_chicken_record_2 = create_inventory_record(session=session, inventory_record=chicken_record_2)

        steak_record = InventoryRecordDB(item_id=saved_steak_item.id, location_id=saved_location.id, quantity=4,
                                             unit=saved_steak_item.default_unit, purchase_date=date(2026,8,4), expiration_date=date(2026,8,10))
        saved_steak_record = create_inventory_record(session=session, inventory_record=steak_record)

        result = get_inventory_record_by_item(session=session, item_id=1)

        assert len(result) == 2
        for item in result:
            assert item.item_id == saved_chicken_item.id
            assert saved_steak_item.id not in result

def test_get_inventory_records_by_item_returns_empty_list_when_no_records_exist():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        household = HouseholdDB(name="Hunt Family")
        saved_household = create_household(session=session, household=household)

        location = LocationDB(household_id=saved_household.id, name="Kitchen")
        saved_location = create_location(session=session, location=location)

        category = CategoryDB(name="Meat", perishable_default=True)
        saved_category = create_category(session=session, category=category)

        chicken_item = ItemDB(name="chicken", category_id=saved_category.id, default_unit="lb")
        saved_chicken_item = create_item(session=session, item=chicken_item)

        steak_item = ItemDB(name="Steak", category_id=saved_category.id, default_unit="lb")
        saved_steak_item = create_item(session=session, item=steak_item)

        result = get_inventory_record_by_item(session=session, item_id=1)

        assert isinstance(result, list)
        assert len(result) == 0