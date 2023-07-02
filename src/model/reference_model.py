from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

from src.model import Base
from src.model.income_model import IncomeModel
from src.model.bill_model import BillModel
from src.model.plan_item_model import PlanItemModel


class IncomeTypeModel(Base):
    __tablename__ = "income_type"

    name: Mapped[str] = mapped_column(primary_key=True)
    income: Mapped[list[IncomeModel]] = relationship(back_populates="income")


class ProviderTypeModel(Base):
    __tablename__ = "provider_type"

    name: Mapped[str] = mapped_column(primary_key=True)

    bill_template: Mapped[list["BillTemplateModel"]] = relationship(back_populates="provider")
    bill: Mapped[list["BillModel"]] = relationship(back_populates="provider")


class PaymentTypeModel(Base):
    __tablename__ = "payment_type"

    name: Mapped[str] = mapped_column(primary_key=True)

    bill_template: Mapped[list[BillTemplateModel]] = relationship(back_populates="payment")
    bill: Mapped[list[BillModel]] = relationship(back_populates="payment")
    plan_item: Mapped[list[PlanItemModel]] = relationship(back_populates="payment")


class BillTemplateModel(Base):
    __tablename__ = "template"

    id_: Mapped[int] = mapped_column("id", primary_key=True)
    provider_type: Mapped[str] = mapped_column(ForeignKey("provider_type.name"), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    due_date: Mapped[int] = mapped_column(nullable=False)
    payment_type: Mapped[str] = mapped_column(ForeignKey("payment_type.name"), nullable=False)
    biweekly: Mapped[bool] = mapped_column(default=False, nullable=False)
    payment: Mapped[PaymentTypeModel] = relationship(back_populates="bill_template")
    provider: Mapped[ProviderTypeModel] = relationship(back_populates="bill_template")
