from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

from src.model import Base
from src.model.budget_model import BudgetModel
from src.model.plan_model import PlanModel
from src.model.reference_model import IncomeTypeModel


class IncomeModel(Base):
    __tablename__ = "income"

    id_: Mapped[UUID] = mapped_column("id", primary_key=True)
    date: Mapped[datetime] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    income_type: Mapped[str] = mapped_column(ForeignKey("income_type.name"), nullable=False)
    budget_id: Mapped[UUID] = mapped_column(ForeignKey("budget.id"), nullable=False)
    plan_id: Mapped[UUID] = mapped_column(ForeignKey("plan.id"), nullable=False)
    is_locked: Mapped[bool] = mapped_column(default=False, nullable=False)

    plan: Mapped[PlanModel] = relationship(back_populates="income")
    budget: Mapped[BudgetModel] = relationship(back_populates="income")
    income: Mapped[IncomeTypeModel] = relationship(back_populates="income")
