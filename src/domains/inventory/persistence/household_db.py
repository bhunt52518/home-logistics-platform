from src.database.base import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class HouseholdDB(Base):
    __tablename__= "households"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement= True)
    name: Mapped[str] = mapped_column(String, nullable=False)
