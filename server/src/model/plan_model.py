from sqlalchemy.dialects.postgresql import UUID

from src.model import db


class PlanModel(db.Model):  # type: ignore[name-defined]
    __tablename__ = "plan"

    id_ = db.Column("id", UUID(as_uuid=True), primary_key=True)
    budget_id = db.Column(db.ForeignKey("budget.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    income = db.relationship("IncomeModel", back_populates="plan")
    is_locked = db.Column(db.Boolean, nullable=False, default=False)
    plan_item = db.relationship("PlanItemModel", back_populates="plan")
