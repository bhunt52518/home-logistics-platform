from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.domains.inventory.models.item_allocation_request import ItemAllocationRequest
from src.domains.inventory.models.inventory_record_response import InventoryRecordResponse
from src.domains.inventory.services.allocation_service import process_allocation
from src.database.session import get_db

router = APIRouter(tags=["Inventory"])

@router.post("/allocations", response_model=list[InventoryRecordResponse])
def post_allocation(allocation_request: ItemAllocationRequest, session: Session = Depends(get_db)):

    try:
        return process_allocation(session=session, allocation_request=allocation_request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
