from src.domains.inventory.models.inventory_record import InventoryRecord
from src.domains.inventory.persistence.household_db import HouseholdDB
from src.domains.inventory.persistence.category_db import CategoryDB
from src.domains.inventory.persistence.location_db import LocationDB
from src.domains.inventory.persistence.item_db import ItemDB
from src.domains.inventory.persistence.inventory_record_db import InventoryRecordDB

from sqlalchemy.orm import Session




def apply_allocations(inventory_records: list[InventoryRecord]) -> list[InventoryRecord]:

    raise NotImplementedError

def create_household(session: Session, household: HouseholdDB) -> HouseholdDB:

    session.add(household)
    session.commit()
    session.refresh(household)

    return household

def create_location(session: Session, location: LocationDB) -> LocationDB:

    session.add(location)
    session.commit()
    session.refresh(location)

    return location

def create_category(session: Session, category: CategoryDB) -> CategoryDB:

    session.add(category)
    session.commit()
    session.refresh(category)

    return category

def create_item(session: Session, item: ItemDB):

    session.add(item)
    session.commit()
    session.refresh(item)

    return item

def create_inventory_record(session: Session, inventory_record: InventoryRecordDB):

    session.add(inventory_record)
    session.commit()
    session.refresh(inventory_record)

    return inventory_record
