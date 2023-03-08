from sqlalchemy.dialects.postgresql import UUID

from src.model import db
from src.model.enums import income_type_enum


class IncomeModel(db.Model):  # type: ignore[name-defined]
    __tablename__ = "income"

    id_ = db.Column("id", UUID(as_uuid=True), primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    income_type = db.Column(income_type_enum, nullable=False)
    budget_id = db.Column(db.ForeignKey("budget.id"), nullable=False)
    plan_id = db.Column(db.ForeignKey("plan.id"), nullable=False)
    is_locked = db.Column(db.Boolean, nullable=False, default=False)
    plan = db.relationship("PlanModel", back_populates="income")
