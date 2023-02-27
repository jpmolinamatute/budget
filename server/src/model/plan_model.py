from sqlalchemy.dialects.postgresql import UUID

from src.model import db
from src.model.enums import payment_type


# @TODO: at the moment there is a Plan dependency on Income, but it should be the other way around.
#  This means we need to delete the foreign key in Plan and add it to Income. Then we need to
# update the PlanController and IncomeController to reflect this change. We also need to update db.
# slq file to reflect this change.


class PlanModel(db.Model):  # type: ignore[name-defined]
    __tablename__ = "payment_plan"
    __table_args__ = (db.UniqueConstraint("payment", "budget_id", "income_id", name="_date"),)

    id_ = db.Column("id", UUID(as_uuid=True), primary_key=True)
    payment = db.Column(payment_type, nullable=False)
    budget_id = db.Column(db.ForeignKey("budget.id"), nullable=False)
    income_id = db.Column(db.ForeignKey("income.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    is_closed = db.Column(db.Boolean, nullable=False, default=False)
    income = db.relationship("IncomeModel", back_populates="payment_plan")
