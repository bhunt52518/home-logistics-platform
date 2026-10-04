from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.database.base import Base

from src.domains.inventory.persistence.category_db import CategoryDB
from src.domains.inventory.persistence.household_db import HouseholdDB
from src.domains.inventory.persistence.inventory_record_db import InventoryRecordDB
from src.domains.inventory.persistence.item_db import ItemDB
from src.domains.inventory.persistence.location_db import LocationDB
from src.domains.shopping.persistence.shopping_list_db import ShoppingListItemDB
from src.domains.shopping.models.shopping_list_item import ShoppingListItem
from src.domains.shopping.models.shopping_list_source import ShoppingListSource
from src.domains.shopping.services.shopping_list_service import (
    add_shopping_list_item, mark_shopping_list_item_as_purchased, find_inventory_match_for_purchased_item,
    create_inventory_item_from_purchase, stock_purchased_item)
from src.domains.inventory.repositories.inventory_repository import get_item
from src.domains.inventory.models.inventory_allocation import InventoryAllocation
from src.domains.shopping.models.stock_purchased_items_request import StockPurchasedItemRequest




def test_manual_purchase_can_be_created_and_stocked_in_inventory() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        household = HouseholdDB(name="Test Household")
        category = CategoryDB(name="Meat", perishable_default=True)

        session.add_all([household, category])
        session.commit()
        session.refresh(household)
        session.refresh(category)

        refrigerator = LocationDB(household_id=household.id, name="Refrigerator")
        freezer = LocationDB(household_id=household.id, name="Freezer")

        session.add_all([refrigerator, freezer])
        session.commit()
        session.refresh(refrigerator)
        session.refresh(freezer)

        assert household.id is not None
        assert category.id is not None
        assert refrigerator.id is not None
        assert freezer.id is not None

        assert refrigerator.household_id == household.id
        assert freezer.household_id == household.id

        shopping_item = ShoppingListItem(item_id=None, name="Chicken", unit="lb", quantity=Decimal("5"), source=ShoppingListSource.MANUAL)

        created_shopping_item = add_shopping_list_item(session=session, shopping_list_item=shopping_item)

        assert created_shopping_item.id is not None
        assert created_shopping_item.item_id is None
        assert created_shopping_item.name == "Chicken"
        assert created_shopping_item.unit == "lb"
        assert created_shopping_item.quantity == Decimal("5")
        assert created_shopping_item.source == ShoppingListSource.MANUAL
        assert created_shopping_item.purchased == False
        assert created_shopping_item.stocked == False
        assert created_shopping_item.completed == False

        purchased_shopping_item = mark_shopping_list_item_as_purchased(session=session, shopping_list_item_id=created_shopping_item.id)

        assert purchased_shopping_item.id == created_shopping_item.id
        assert purchased_shopping_item.item_id == None
        assert purchased_shopping_item.purchased == True
        assert purchased_shopping_item.stocked == False
        assert purchased_shopping_item.completed == False

        inventory_match = find_inventory_match_for_purchased_item(session=session, shopping_list_item_id=purchased_shopping_item.id)

        assert inventory_match is None

        linked_shopping_item = create_inventory_item_from_purchase(
            session=session, shopping_list_item_id=purchased_shopping_item.id, category_id=category.id
            )
        linked_inventory_match = get_item(session=session, item_id=linked_shopping_item.item_id)

        assert linked_shopping_item.item_id is not None
        assert linked_inventory_match is not None
        assert linked_inventory_match.id == linked_shopping_item.item_id
        assert linked_inventory_match.name == "Chicken"
        assert linked_inventory_match.category_id == category.id
        assert linked_inventory_match.default_unit == "lb"

        refrigerator_allocation = InventoryAllocation(location_id=refrigerator.id, quantity=Decimal("2"))
        freezer_allocation = InventoryAllocation(location_id=freezer.id, quantity=Decimal("3"))

        stock_request = StockPurchasedItemRequest(allocations=[refrigerator_allocation, freezer_allocation])

        stocked_shopping_item = stock_purchased_item(
            session=session, shopping_list_item_id=linked_shopping_item.id, stock_request=stock_request)

        assert stocked_shopping_item.purchased == True
        assert stocked_shopping_item.stocked == True
        assert stocked_shopping_item.completed == False
        assert stocked_shopping_item.item_id == linked_shopping_item.item_id

        inventory_item_records = session.query(InventoryRecordDB).filter(InventoryRecordDB.item_id==linked_shopping_item.item_id).all()

        assert len(inventory_item_records) == 2

        inventory_by_location = {
            item.location_id: item
            for item in inventory_item_records
        }

        assert inventory_by_location[refrigerator.id].quantity == Decimal("2")
        assert inventory_by_location[refrigerator.id].unit == "lb"

        assert inventory_by_location[freezer.id].quantity == Decimal("3")
        assert inventory_by_location[freezer.id].unit == "lb"


