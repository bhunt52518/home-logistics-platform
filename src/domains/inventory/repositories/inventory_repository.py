from src.domains.inventory.models.inventory_record import InventoryRecord
from src.domains.inventory.models.category_create import CategoryCreate
from src.domains.inventory.persistence.category_db import CategoryDB
from src.domains.inventory.models.location_create import LocationCreate
from src.domains.inventory.persistence.location_db import LocationDB
from src.domains.inventory.persistence.item_db import ItemDB
from src.domains.inventory.persistence.inventory_record_db import InventoryRecordDB
from src.domains.inventory.models.household_create import HouseholdCreate
from src.domains.inventory.persistence.household_db import HouseholdDB

from src.domains.inventory.models.item import Item

from sqlalchemy.orm import Session




def apply_allocations(session: Session, inventory_records: list[InventoryRecord]) -> list[InventoryRecordDB]:
    inventory_records_dbs: list[InventoryRecordDB] = []

    for inventory_record in inventory_records:
        inventory_record_db = InventoryRecordDB(item_id=inventory_record.item_id, location_id=inventory_record.location_id, quantity=inventory_record.quantity,
                                                unit=inventory_record.unit, purchase_date=inventory_record.purchase_date, expiration_date=inventory_record.expiration_date)

        inventory_records_dbs.append(inventory_record_db)
        session.add(inventory_record_db)

    try:
        session.commit()
    except Exception:
        session.rollback()
        raise

    for inventory_record_db in inventory_records_dbs:
        session.refresh(inventory_record_db)

    return inventory_records_dbs

def create_household(session: Session, household: HouseholdCreate) -> HouseholdDB:
    household_db = HouseholdDB(name=household.name)

    session.add(household_db)
    session.commit()
    session.refresh(household_db)

    return household_db

def get_household(session: Session, household_id: int) -> HouseholdDB | None:

    return session.get(HouseholdDB, household_id)

def create_location(session: Session, location: LocationCreate) -> LocationDB:
    location_db = LocationDB(household_id=location.household_id, name=location.name)
    
    session.add(location_db)
    session.commit()
    session.refresh(location_db)

    return location_db

def get_location(session: Session, location_id: int) -> LocationDB | None:

    return session.get(LocationDB, location_id)

def create_category(session: Session, category: CategoryCreate) -> CategoryDB:
    category_db = CategoryDB(name=category.name, perishable_default=category.perishable_default)

    session.add(category_db)
    session.commit()
    session.refresh(category_db)

    return category_db

def get_category(session: Session, category_id: int) -> CategoryDB | None:

    return session.get(CategoryDB, category_id)

def create_item(session: Session, item: Item) -> ItemDB:
    item_db = ItemDB(name=item.name, category_id=item.category_id, default_unit=item.default_unit)

    session.add(item_db)
    session.commit()
    session.refresh(item_db)

    return item_db

def create_inventory_record(session: Session, inventory_record: InventoryRecordDB):

    session.add(inventory_record)
    session.commit()
    session.refresh(inventory_record)

    return inventory_record
