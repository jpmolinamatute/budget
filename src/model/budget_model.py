from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint

from src.model import Base


class BudgetModel(Base):
    __tablename__ = "budget"
    __table_args__ = (UniqueConstraint("year", "month", name="_date"),)

    id_: Mapped[UUID] = mapped_column("id", primary_key=True)
    month: Mapped[int] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    is_locked: Mapped[bool] = mapped_column(default=False, nullable=False)

    plan: Mapped[list["PlanModel"]] = relationship(back_populates="budget")
    bill: Mapped[list["BillModel"]] = relationship(back_populates="budget")
    income: Mapped[list["IncomeModel"]] = relationship(back_populates="budget")
