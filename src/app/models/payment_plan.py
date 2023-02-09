from sqlalchemy.dialects.postgresql import UUID

from src.app.models import db

from src.app.models.enums import payment_type


class PaymentPlan(db.Model):  # type: ignore[name-defined]
    __tablename__ = "payment_plan"

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    payment = db.Column(payment_type, nullable=False)
    budget_id = db.Column(db.ForeignKey("budget.id"), nullable=False)
    salary_id = db.Column(db.ForeignKey("salary.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)

    budget = db.relationship("Budget", back_populates="payment_plan")
    salary = db.relationship("Salary", back_populates="payment_plan")
