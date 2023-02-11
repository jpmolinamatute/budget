from sqlalchemy.dialects.postgresql import UUID

from src.app.model import db


class SalaryModel(db.Model):  # type: ignore[name-defined]
    __tablename__ = "salary"

    id_ = db.Column("id", UUID(as_uuid=True), primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    extra = db.Column(db.Float, nullable=False, default=0.0)
    budget_id = db.Column(db.ForeignKey("budget.id"), nullable=False)

    budget = db.relationship("Budget", back_populates="salary")
    payment_plan = db.relationship("PaymentPlan", back_populates="salary")
