from src.database.base import Base
from src.domains.shopping.models.shopping_list_source import ShoppingListSource

from sqlalchemy import Integer, String, ForeignKey, Numeric, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column

from decimal import Decimal





class ShoppingListItemDB(Base):
    __tablename__ = "shopping_list_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("items.id"), nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    unit: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[ShoppingListSource] = mapped_column(Enum(ShoppingListSource), nullable=False)
    purchased: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
