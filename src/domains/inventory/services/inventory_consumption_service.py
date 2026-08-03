from sqlalchemy.orm import Session

from src.domains.inventory.persistence.inventory_record_db import InventoryRecordDB
from src.domains.inventory.models.inventory_consumption_request import InventoryConsumptionRequest
from src.domains.inventory.repositories.inventory_repository import get_inventory_record, update_inventory_record


def consume_inventory(session: Session, consumption_request: InventoryConsumptionRequest) -> InventoryRecordDB:
    inventory_record = get_inventory_record(session=session, inventory_record_id=consumption_request.inventory_record_id)

    if inventory_record is None:
        raise ValueError("Record does not exist.")

    if consumption_request.quantity > inventory_record.quantity:
        raise ValueError("Consumption amount can not exceed inventory quantity")


    inventory_record.quantity = inventory_record.quantity - consumption_request.quantity

    return update_inventory_record(session=session, inventory_record=inventory_record)

    
