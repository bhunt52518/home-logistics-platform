from src.database.base import Base

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column


class CategoryDB(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    perishable_default: Mapped[bool] = mapped_column(Boolean, nullable=False)