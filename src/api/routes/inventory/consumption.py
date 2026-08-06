from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.domains.inventory.models.inventory_consumption_request import InventoryConsumptionRequest
from src.domains.inventory.persistence.inventory_record_db import InventoryRecordDB
from src.domains.inventory.services.inventory_consumption_service import consume_inventory
from src.domains.inventory.models.inventory_record_response import InventoryRecordResponse





router = APIRouter(tags=["Inventory"])

@router.post("/consume", response_model=InventoryRecordResponse, status_code=200)

def post_inventory_record(consumption_request: InventoryConsumptionRequest, session: Session=Depends(get_db)) -> InventoryRecordDB:

    try:
        return consume_inventory(session=session, consumption_request=consumption_request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))from error