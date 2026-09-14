from src.domains.shopping.models.shopping_list_item import ShoppingListItem
from src.domains.shopping.models.stock_purchased_items_request import StockPurchasedItemRequest
from src.domains.shopping.persistence.shopping_list_db import ShoppingListItemDB
from src.domains.shopping.models.shopping_list_merge_suggestion import ShoppingListMergeSuggestion
from src.domains.inventory.models.item_allocation_request import ItemAllocationRequest
from src.domains.inventory.services.allocation_service import process_allocation
from src.domains.shopping.repositories.shopping_repository import (
    get_duplicate_shopping_list_item, create_shopping_list_item, get_shopping_list_item, update_shopping_list_quantity,
    get_active_shopping_list_items, update_shopping_list_item_as_purchased, get_purchased_shopping_list_items,
    update_shopping_list_item_as_stocked)

from sqlalchemy.orm import Session




def add_shopping_list_item(session: Session, shopping_list_item: ShoppingListItem) -> ShoppingListItemDB | ShoppingListMergeSuggestion:
    list_canidate_db = ShoppingListItemDB(
        name=shopping_list_item.name, quantity=shopping_list_item.quantity, unit=shopping_list_item.unit, source=shopping_list_item.source,
        item_id=shopping_list_item.item_id, purchased=shopping_list_item.purchased
    )
    duplicate = get_duplicate_shopping_list_item(session=session, shopping_list_db=list_canidate_db)

    if duplicate is None:
        return create_shopping_list_item(session=session, shopping_list=shopping_list_item)
    else:
        merged_quantity = duplicate.quantity + shopping_list_item.quantity

        merge_suggestion = ShoppingListMergeSuggestion(
            shopping_list_item_id=duplicate.item_id, existing_quantity=duplicate.quantity, requested_quantity=shopping_list_item.quantity,
            merged_quantity=merged_quantity, name=duplicate.name, unit=duplicate.unit
        )
        return merge_suggestion

def approve_shopping_list_merge_suggestion(session: Session, merge_suggestion: ShoppingListMergeSuggestion) -> ShoppingListItemDB:
    existing_item = get_shopping_list_item(session=session, shopping_list_id=merge_suggestion.shopping_list_item_id)

    if existing_item is None:
        raise ValueError("Shopping list item does not exist.")
    if existing_item.quantity != merge_suggestion.existing_quantity:
        raise ValueError("Existing quantity does not match.")

    return update_shopping_list_quantity(session=session, shopping_list=existing_item, quantity=merge_suggestion.merged_quantity)

def get_active_shopping_list(session: Session) -> list[ShoppingListItemDB]:
    active_shopping_list = get_active_shopping_list_items(session=session)

    return active_shopping_list

def mark_shopping_list_item_as_purchased(session: Session, shopping_list_item_id: int) -> ShoppingListItemDB:
    updated_shopping_list_item = update_shopping_list_item_as_purchased(
        session=session, shopping_list_item_id=shopping_list_item_id, purchased=True)

    return updated_shopping_list_item

def get_purchased_items(session: Session) -> list[ShoppingListItemDB]:
    purchased_items = get_purchased_shopping_list_items(session=session)

    return purchased_items

def stock_purchased_item(session: Session, shopping_list_item_id: int, stock_request: StockPurchasedItemRequest) -> ShoppingListItemDB:
    shopping_item_to_stock = get_shopping_list_item(session=session, shopping_list_id=shopping_list_item_id)

    if shopping_item_to_stock is None:
        raise ValueError("Shopping list item does not exist.")
    elif shopping_item_to_stock.purchased is False:
        raise ValueError("Shopping list item has not be purchased.")
    elif shopping_item_to_stock.stocked is True:
        raise ValueError("Shopping item has already been stocked.")
    elif shopping_item_to_stock.item_id is None:
        raise ValueError("Shopping list item is not linked to an inventory item.")

    allocation_request = ItemAllocationRequest(
        item_id=shopping_item_to_stock.item_id, purchased_quantity=shopping_item_to_stock.quantity,
        item_unit=shopping_item_to_stock.unit, allocations=stock_request.allocations
    )

    process_allocation(session=session, allocation_request=allocation_request)

    stocked_item = update_shopping_list_item_as_stocked(
        session=session, shopping_list_item_id=shopping_item_to_stock.id, stocked=True)

    return stocked_item