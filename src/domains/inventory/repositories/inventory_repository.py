from src.domains.inventory.models.inventory_record import InventoryRecord


def apply_allocations(inventory_records: list[InventoryRecord]) -> list[InventoryRecord]:

    _inventory_records: list[InventoryRecord] = []

    _inventory_records.extend(inventory_records)