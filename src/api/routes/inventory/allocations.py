from fastapi import APIRouter

from src.domains.inventory.models.item_allocation_request import ItemAllocationRequest
from src.domains.inventory.services.allocation_service import is_allocation_valid

router = APIRouter(tags=["Inventory"])

@router.post("/allocations")
def post_allocation(allocation_request: ItemAllocationRequest):

    result = is_allocation_valid(allocation_request= allocation_request)

    if result:
        message = "Allocation is valid."
    else:
        message = "Allocation quantity does not equal purchased quntity."
    return {
        "valid": result,
        "message": message,
    }