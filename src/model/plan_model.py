from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

from src.model import Base
from src.model.budget_model import BudgetModel


class PlanModel(Base):
    __tablename__ = "plan"

    id_: Mapped[UUID] = mapped_column("id", primary_key=True)
    budget_id: Mapped[UUID] = mapped_column(ForeignKey("budget.id"), nullable=False)
    start_date: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[datetime] = mapped_column(nullable=False)
    is_locked: Mapped[bool] = mapped_column(default=False, nullable=False)

    budget: Mapped[BudgetModel] = relationship(back_populates="plan")
    income: Mapped[list["IncomeModel"]] = relationship(back_populates="plan")
    plan_item: Mapped[list["PlanItemModel"]] = relationship(back_populates="plan")
