from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.domains.inventory.models.location_create import LocationCreate
from src.domains.inventory.persistence.location_db import LocationDB
from src.domains.inventory.services.location_service import (create_inventory_location)
from src.domains.inventory.models.location_response import LocationResponse





router = APIRouter(tags=["Inventory"])

@router.post("/location", response_model=LocationResponse, status_code=201)

def post_location(location_request: LocationCreate, session: Session = Depends(get_db)) -> LocationDB:

    try:
        return create_inventory_location(session=session, household_id=location_request.household_id, name=location_request.name,)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error),)from error

