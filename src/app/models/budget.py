from sqlalchemy.dialects.postgresql import UUID

from src.app.models import db


class Budget(db.Model):  # type: ignore[name-defined]
    __tablename__ = "budget"
    __table_args__ = (db.UniqueConstraint("year", "month", name="_date"),)

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    is_current = db.Column(db.Boolean, nullable=False)

    bill = db.relationship("Bill", back_populates="budget")
    salary = db.relationship("Salary", back_populates="budget")
    payment_plan = db.relationship("PaymentPlan", back_populates="budget")
