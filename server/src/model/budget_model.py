from sqlalchemy.dialects.postgresql import UUID

from src.model import db


class BudgetModel(db.Model):  # type: ignore[name-defined]
    __tablename__ = "budget"
    __table_args__ = (db.UniqueConstraint("year", "month", name="_date"),)

    id_ = db.Column("id", UUID(as_uuid=True), primary_key=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_current = db.Column(db.Boolean, nullable=False)
