from sqlalchemy.dialects.postgresql import UUID

from src.app.model import db
from src.app.model.enums import payment_type


class PaymentPlanModel(db.Model):  # type: ignore[name-defined]
    __tablename__ = "payment_plan"

    id_ = db.Column("id", UUID(as_uuid=True), primary_key=True)
    payment = db.Column(payment_type, nullable=False)
    budget_id = db.Column(db.ForeignKey("budget.id"), nullable=False)
    salary_id = db.Column(db.ForeignKey("salary.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)