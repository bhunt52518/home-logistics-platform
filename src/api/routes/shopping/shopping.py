from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.domains.shopping.models.shopping_list_item_response import ShoppingListItemResponse
from src.domains.shopping.models.shopping_list_merge_suggestion_response import ShoppingListMergeSuggestionResponse
from src.domains.shopping.models.shopping_list_item import ShoppingListItem
from src.domains.shopping.models.shopping_list_merge_suggestion import ShoppingListMergeSuggestion
from src.domains.shopping.services.shopping_list_service import (
    add_shopping_list_item, approve_shopping_list_merge_suggestion, get_active_shopping_list, mark_shopping_list_item_as_purchased
)
from src.database.session import get_db





router = APIRouter(tags=["Shopping"])

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

@router.get(
    "/list", response_model= list[ShoppingListItemResponse], status_code=200
)

def get_shopping_list(session: Session=Depends(get_db)) -> list[ShoppingListItemResponse]:

    try:
        return get_active_shopping_list(session=session)
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