from sqlalchemy.orm import Session

from src.domains.inventory.repositories.inventory_repository import get_item, get_inventory_record_by_item
from src.domains.inventory.persistence.inventory_record_db import InventoryRecordDB
from src.domains.inventory.models.item_quantity_response import ItemQuantityResponse
from decimal import Decimal





def get_item_inventory_quantity(session: Session, item_id: int) -> ItemQuantityResponse:
    item = get_item(session=session, item_id=item_id)

    if item is None:
        raise ValueError("Item does not exist.")

    inventory_records = get_inventory_record_by_item(session=session, item_id=item_id)

    item_quantity = Decimal("0")

    for record in inventory_records:
        item_quantity += record.quantity

    total_item_quantity = ItemQuantityResponse(name=item.name, total_quantity=item_quantity, unit=item.default_unit)

    return total_item_quantity