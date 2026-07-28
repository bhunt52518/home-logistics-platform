from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.domains.inventory.models.household_create import HouseholdCreate
from src.domains.inventory.persistence.household_db import HouseholdDB
from src.domains.inventory.services.household_service import (create_inventory_household)
from src.domains.inventory.models.household_response import HouseholdResponse





router = APIRouter(tags=["Inventory"])

@router.post("/households", response_model=HouseholdResponse, status_code=201)

def post_household(household_request: HouseholdCreate, session: Session = Depends(get_db)) -> HouseholdDB:
    return create_inventory_household(session=session, name=household_request.name,)