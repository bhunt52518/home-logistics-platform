from src.domains.shopping.models.shopping_list_item import ShoppingListItem
from src.domains.shopping.persistence.shopping_list_db import ShoppingListItemDB

from src.core.services.name_validator import NameValidator

from sqlalchemy.orm import Session
from sqlalchemy import func



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

def get_dulicate_shopping_list_item (session: Session, shopping_list_db: ShoppingListItemDB) -> ShoppingListItemDB | None:

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
