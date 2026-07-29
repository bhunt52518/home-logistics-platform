from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.domains.inventory.models.category_create import CategoryCreate
from src.domains.inventory.persistence.category_db import CategoryDB
from src.domains.inventory.services.category_service import (create_inventory_category)
from src.domains.inventory.models.category_response import CategoryResponse





router = APIRouter(tags=["Inventory"])

@router.post("/category", response_model=CategoryResponse, status_code=201)

def post_category(category_request: CategoryCreate, session: Session = Depends(get_db)) -> CategoryDB:
    return create_inventory_category(session=session, name=category_request.name, perishable_default=category_request.perishable_default)
