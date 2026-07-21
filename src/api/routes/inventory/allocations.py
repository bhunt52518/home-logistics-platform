from fastapi import APIRouter

from src.domains.inventory.models.item_allocation_request import ItemAllocationRequest

router = APIRouter(tags=["Inventory"])

@router.post("/allocations")
def post_allocation(allocation_request: ItemAllocationRequest):
    return allocation_request