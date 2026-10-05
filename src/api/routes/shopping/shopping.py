from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.domains.shopping.models.shopping_list_item_response import ShoppingListItemResponse
from src.domains.shopping.models.create_inventory_item_from_purchase_request import CreateInventoryItemFromPurchaseRequest
from src.domains.shopping.models.shopping_list_merge_suggestion_response import ShoppingListMergeSuggestionResponse
from src.domains.shopping.models.shopping_list_item import ShoppingListItem
from src.domains.shopping.models.shopping_list_merge_suggestion import ShoppingListMergeSuggestion
from src.domains.shopping.models.stock_purchased_items_request import StockPurchasedItemRequest
from src.domains.shopping.services.shopping_list_service import (
    add_shopping_list_item, approve_shopping_list_merge_suggestion, get_active_shopping_list, mark_shopping_list_item_as_purchased,
    get_purchased_items, stock_purchased_item, complete_purchased_item, link_purchased_item_to_inventory, find_inventory_match_for_purchased_item,
    create_inventory_item_from_purchase
)
from src.domains.inventory.models.item_reposne import ItemResponse
from src.database.session import get_db





router = APIRouter(tags=["Shopping"])

@router.get(
    "/list", response_model= list[ShoppingListItemResponse], status_code=200
)

def get_shopping_list(session: Session=Depends(get_db)) -> list[ShoppingListItemResponse]:

    try:
        return get_active_shopping_list(session=session)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

@router.get(
        "/list/purchased", response_model=list[ShoppingListItemResponse], status_code=200
)

def get_purchased_list(session: Session=Depends(get_db)) -> list[ShoppingListItemResponse]:
    try:
        return get_purchased_items(session=session)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

@router.get(
        "/item/{shopping_list_item_id}/inventory-match", response_model=ItemResponse | None, status_code=200
)

def get_inventory_match_for_purchased_item(shopping_list_item_id: int, session: Session=Depends(get_db)):
    try:
        return find_inventory_match_for_purchased_item(session=session, shopping_list_item_id=shopping_list_item_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

@router.patch(
    "/item/{shopping_list_item_id}/purchased", response_model=ShoppingListItemResponse, status_code=200
)

def patch_shopping_list_item_as_purchased(shopping_list_item_id: int, session: Session=Depends(get_db)):
    try:
        return mark_shopping_list_item_as_purchased(session=session, shopping_list_item_id=shopping_list_item_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

@router.patch(
        "/item/{shopping_list_item_id}/complete", response_model=ShoppingListItemResponse, status_code=200
)

def patch_shopping_list_item_as_completed(shopping_list_item_id: int, session: Session=Depends(get_db)):
    try:
        return complete_purchased_item(session=session, shopping_list_item_id=shopping_list_item_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

@router.patch(
        "/item/{shopping_list_item_id}/linked", response_model=ShoppingListItemResponse, status_code=200
)
def patch_linked_item(shopping_list_item_id: int, item_id: int,session: Session=Depends(get_db)):
    try:
        return link_purchased_item_to_inventory(session=session, shopping_list_item_id=shopping_list_item_id, item_id=item_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error    

@router.post(
    "/item", response_model= ShoppingListItemResponse | ShoppingListMergeSuggestion,
    status_code=200
)

def post_add_shopping_list_item(shopping_list_item: ShoppingListItem, session: Session=Depends(get_db)):
    try:
        return add_shopping_list_item(session=session, shopping_list_item=shopping_list_item)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

@router.post(
    "/merge/approve", response_model=ShoppingListItemResponse, status_code=200
)

def post_approve_shopping_list_merge_suggestion(merge_suggestion: ShoppingListMergeSuggestion, session: Session=Depends(get_db)):
    try:
        return approve_shopping_list_merge_suggestion(session=session, merge_suggestion=merge_suggestion)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post(
    "/item/{shopping_list_item_id}/stock", response_model=ShoppingListItemResponse, status_code=200
)

def post_stock_purchased_item(shopping_list_item_id: int, stock_request:StockPurchasedItemRequest, session: Session=Depends(get_db)):
    try:
        return stock_purchased_item(session=session, shopping_list_item_id=shopping_list_item_id, stock_request=stock_request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

@router.post(
    "/item/{shopping_list_item_id}/inventory", response_model=ShoppingListItemResponse, status_code=200
)

def post_inventory_item_from_purchase(shopping_list_item_id: int, request: CreateInventoryItemFromPurchaseRequest, session: Session=Depends(get_db)):
    try:
        return create_inventory_item_from_purchase(
            session=session, shopping_list_item_id=shopping_list_item_id,category_id=request.category_id,
            restock_point=request.restock_point, target_stock=request.target_stock)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error