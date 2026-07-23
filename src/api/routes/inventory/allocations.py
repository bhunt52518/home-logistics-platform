from fastapi import APIRouter

from src.domains.inventory.models.item_allocation_request import ItemAllocationRequest
from src.domains.inventory.services.allocation_service import is_allocation_valid

router = APIRouter(tags=["Inventory"])

@router.post("/allocations")
def post_allocation(allocation_request: ItemAllocationRequest):

    result = is_allocation_valid(allocation_request= allocation_request)
    return {
        "valid": result,
    }