from sqlalchemy.orm import Mapped, mapped_column

from src.model import Base
from src.model.enums import PaymentType, ProviderType


class BillTemplateModel(Base):
    __tablename__ = "template"

    id_: Mapped[int] = mapped_column("id", primary_key=True)
    provider: Mapped[ProviderType] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    due_date: Mapped[int] = mapped_column(nullable=False)
    payment: Mapped[PaymentType] = mapped_column(nullable=False)
    biweekly: Mapped[bool] = mapped_column(default=False, nullable=False)
