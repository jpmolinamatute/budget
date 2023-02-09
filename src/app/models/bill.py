from sqlalchemy.dialects.postgresql import UUID

from src.app.models import db

from src.app.models.enums import provider_type, payment_type


class Bill(db.Model):  # type: ignore[name-defined]
    __tablename__ = "bill"

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    budget_id = db.Column(db.ForeignKey("budget.id"), nullable=False)
    provider = db.Column(provider_type, nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    due_date = db.Column(db.Date, nullable=False)
    payment = db.Column(payment_type, nullable=False)
    is_paid = db.Column(db.Boolean, nullable=False, default=False)

    budget = db.relationship("Budget", back_populates="bill")
