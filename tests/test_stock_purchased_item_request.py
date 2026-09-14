from src.domains.shopping.models.stock_purchased_items_request import StockPurchasedItemRequest
from src.domains.inventory.models.inventory_allocation import InventoryAllocation

from decimal import Decimal




def test_stock_purchased_item_request_with_valid_allocations():
    request = StockPurchasedItemRequest(
        allocations=[
            InventoryAllocation(
                location_id=1,
                quantity=Decimal("2")
            ),
            InventoryAllocation(
                location_id=2,
                quantity=Decimal("3")
            )
        ]
    )

    assert len(request.allocations) == 2
    assert request.allocations[0].location_id == 1
    assert request.allocations[0].quantity == Decimal("2")
    assert request.allocations[1].location_id == 2
    assert request.allocations[1].quantity == Decimal("3")