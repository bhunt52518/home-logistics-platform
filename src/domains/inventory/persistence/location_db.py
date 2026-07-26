from src.database.base import Base

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column



class LocationDB(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    household_id: Mapped[int] = mapped_column(ForeignKey("households.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    