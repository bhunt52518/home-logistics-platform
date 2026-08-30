from sqlalchemy.orm import Session

from src.domains.inventory.repositories.inventory_repository import get_item
from src.domains.inventory.services.item_inventory_quantity_service import get_item_inventory_quantity
from src.domains.inventory.models.restock_status_response import RestockStatusResponse
from src.domains.inventory.repositories.inventory_repository import get_items_with_restock_point
from decimal import Decimal





def get_restock_status(session: Session, item_id: int) -> RestockStatusResponse:
    item = get_item(session=session, item_id=item_id)
    if item is None:
        raise ValueError("Item does not exist.")
    item_quantity = get_item_inventory_quantity(session=session, item_id=item_id)

    needs_restock = False
    if item.restock_point is not None:
        needs_restock = item_quantity.total_quantity <= item.restock_point

    suggested_purchase_quantity = None
    if needs_restock:
        if item.target_stock is not None:
            suggested_purchase_quantity = item.target_stock - item_quantity.total_quantity
        else:
            suggested_purchase_quantity = (item.restock_point - item_quantity.total_quantity) + Decimal("1")
        suggested_purchase_quantity = max(suggested_purchase_quantity, Decimal("0"))

    restock_status = RestockStatusResponse(
        name=item.name, current_quantity=item_quantity.total_quantity, unit=item_quantity.unit, restock_point=item.restock_point,
        target_stock=item.target_stock, needs_restock=needs_restock, suggested_purchase_quantity=suggested_purchase_quantity
    )
    
    return restock_status

def get_items_needing_restock(session: Session) -> list[RestockStatusResponse]:
    items = get_items_with_restock_point(session=session)

    items_needing_restock = []

    for item in items:
        restock_status = get_restock_status(session=session, item_id=item.id)
        if restock_status.needs_restock is True:
            items_needing_restock.append(restock_status)

    return items_needing_restock
