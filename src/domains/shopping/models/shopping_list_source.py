from enum import Enum




class ShoppingListSource(str, Enum):
    MANUAL = "manual"
    RESTOCK = "restock"