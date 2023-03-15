from sqlalchemy.dialects.postgresql import UUID

from src.model import db
from src.model.enums import payment_type


class PlanItemModel(db.Model):  # type: ignore[name-defined]
    __tablename__ = "plan_item"
    __table_args__ = (db.UniqueConstraint("payment", "plan_id", name="_date"),)

    id_ = db.Column("id", UUID(as_uuid=True), primary_key=True)
    payment = db.Column(payment_type, nullable=False)
    plan_id = db.Column(db.ForeignKey("plan.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    plan = db.relationship("PlanModel", back_populates="plan_item")
