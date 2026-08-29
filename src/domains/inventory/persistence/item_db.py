from src.database.base import Base

from sqlalchemy import Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from decimal import Decimal

class ItemDB(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
    default_unit: Mapped[str] = mapped_column(String, nullable=False)
    restock_point: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)