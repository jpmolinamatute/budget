from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey, UniqueConstraint

from src.model import Base
from src.model.plan_model import PlanModel
from src.model.reference_model import PaymentTypeModel


class PlanItemModel(Base):
    __tablename__ = "plan_item"
    __table_args__ = (UniqueConstraint("payment_type", "plan_id", name="_date"),)

    id_: Mapped[UUID] = mapped_column("id", primary_key=True)
    payment_type: Mapped[str] = mapped_column(ForeignKey("payment_type.name"), nullable=False)
    plan_id: Mapped[UUID] = mapped_column(ForeignKey("plan.id"), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)

    plan: Mapped[PlanModel] = relationship(back_populates="plan_item")
    payment: Mapped[PaymentTypeModel] = relationship(back_populates="plan_item")
