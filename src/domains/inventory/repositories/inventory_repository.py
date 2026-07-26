from src.domains.inventory.models.inventory_record import InventoryRecord
from src.domains.inventory.persistence.household_db import HouseholdDB
from src.domains.inventory.persistence.category_db import CategoryDB
from src.domains.inventory.persistence.location_db import LocationDB

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