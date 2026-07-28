from src.database.base import Base
from src.database.engine import engine

from src.domains.inventory.persistence.category_db import CategoryDB
from src.domains.inventory.persistence.household_db import HouseholdDB
from src.domains.inventory.persistence.inventory_record_db import InventoryRecordDB
from src.domains.inventory.persistence.item_db import ItemDB
from src.domains.inventory.persistence.location_db import LocationDB





def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)