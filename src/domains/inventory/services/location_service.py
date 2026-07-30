from sqlalchemy.orm import Session

from src.domains.inventory.models.location_create import LocationCreate
from src.domains.inventory.persistence.location_db import LocationDB
from src.domains.inventory.repositories.inventory_repository import create_location
from src.domains.inventory.repositories.inventory_repository import get_household




#-----------------------------------------------------------------------------------
# Create
#-----------------------------------------------------------------------------------




def create_inventory_location(session: Session, household_id: int, name: str) -> LocationDB:
    location = LocationCreate(household_id=household_id, name=name)

    household = get_household(session=session, household_id=household_id)
    if household is None:
        raise ValueError("Household does not exist.")

    return create_location(session=session, location=location)