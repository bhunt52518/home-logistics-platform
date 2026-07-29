from sqlalchemy.orm import Session

from src.domains.inventory.models.household_create import HouseholdCreate
from src.domains.inventory.persistence.household_db import HouseholdDB
from src.domains.inventory.repositories.inventory_repository import create_household




#-----------------------------------------------------------------------------------
# Create
#-----------------------------------------------------------------------------------



def create_inventory_household(session: Session, name:str) ->HouseholdDB:
    household = HouseholdCreate(name=name)

    return create_household(session=session, household=household)

