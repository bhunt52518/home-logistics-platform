from src.domains.shopping.models.shopping_list_item import ShoppingListItem
from src.domains.shopping.persistence.shopping_list_db import ShoppingListItemDB

from src.core.services.name_validator import NameValidator

from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal



def create_shopping_list_item(session: Session, shopping_list: ShoppingListItem) -> ShoppingListItemDB:
    shopping_list_db = ShoppingListItemDB(
        name=shopping_list.name, quantity=shopping_list.quantity, unit=shopping_list.unit,
        source=shopping_list.source, item_id=shopping_list.item_id, purchased=shopping_list.purchased
    )

    session.add(shopping_list_db)
    session.commit()
    session.refresh(shopping_list_db)

    return shopping_list_db

def get_shopping_list_item(session: Session, shopping_list_id: int) -> ShoppingListItemDB | None:

    return session.get(ShoppingListItemDB, shopping_list_id)

def get_duplicate_shopping_list_item (session: Session, shopping_list_db: ShoppingListItemDB) -> ShoppingListItemDB | None:

    if shopping_list_db.item_id is not None:
        same_item_id = session.query(ShoppingListItemDB).filter(
            ShoppingListItemDB.item_id==shopping_list_db.item_id,
            ShoppingListItemDB.purchased==False).first()
        return same_item_id
    
    else:
        cleaned_name = NameValidator.validate_non_empty(shopping_list_db.name).lower()
        cleaned_unit = NameValidator.validate_non_empty(shopping_list_db.unit).lower()
        duplicate_item = session.query(ShoppingListItemDB).filter(
            func.lower(ShoppingListItemDB.name)==cleaned_name,
            func.lower(ShoppingListItemDB.unit)==cleaned_unit,
            ShoppingListItemDB.purchased==False
        ).first()
        return duplicate_item

def update_shopping_list_quantity(session: Session, shopping_list: ShoppingListItemDB, quantity: Decimal) -> ShoppingListItemDB:
    shopping_list.quantity=quantity
    
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise

    session.refresh(shopping_list)

    return shopping_list
