from sqlalchemy.orm import Session

from src.domains.inventory.models.category_create import CategoryCreate
from src.domains.inventory.persistence.category_db import CategoryDB
from src.domains.inventory.repositories.inventory_repository import create_category




#--------------------------------------------------------------------------------------
# Create
#--------------------------------------------------------------------------------------




def create_inventory_category(session: Session, name:str, perishable_default: bool) -> CategoryDB:
    category = CategoryCreate(name=name, perishable_default=perishable_default)

    return create_category(session=session, category=category)