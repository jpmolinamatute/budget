from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

from src.model import Base
from src.model.budget_model import BudgetModel
from src.model.enums import PaymentType, ProviderType


class BillModel(Base):
    __tablename__ = "bill"

    id_: Mapped[UUID] = mapped_column("id", primary_key=True)
    budget_id: Mapped[UUID] = mapped_column(ForeignKey("budget.id"), nullable=False)
    provider: Mapped[ProviderType] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    due_date: Mapped[datetime] = mapped_column(nullable=False)
    payment: Mapped[PaymentType] = mapped_column(nullable=False)
    is_locked: Mapped[bool] = mapped_column(default=False, nullable=False)

    budget: Mapped[BudgetModel] = relationship(back_populates="bill")
