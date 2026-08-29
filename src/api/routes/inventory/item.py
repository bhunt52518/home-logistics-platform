from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.domains.inventory.models.item_create import ItemCreate
from src.domains.inventory.models.item_reposne import ItemResponse
from src.domains.inventory.persistence.item_db import ItemDB
from src.domains.inventory.services.item_service import (create_inventory_item)
from src.domains.inventory.services.item_inventory_quantity_service import get_item_inventory_quantity
from src.domains.inventory.models.item_quantity_response import ItemQuantityResponse





router = APIRouter(tags=["Inventory"])

@router.post("/item", response_model=ItemResponse, status_code=201)

def post_item(item_request: ItemCreate, session: Session=Depends(get_db)) -> ItemDB:

    try:
        return create_inventory_item(session=session, category_id=item_request.category_id, name=item_request.name,
                                     default_unit=item_request.default_unit, restock_point=item_request.restock_point)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))from error

@router.get("/item/{item_id}/quantity", response_model=ItemQuantityResponse, status_code=200)

def get_item_quantity(item_id: int, session: Session=Depends(get_db)) -> ItemQuantityResponse:

    try: 
        return get_item_inventory_quantity(session=session, item_id=item_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))from error