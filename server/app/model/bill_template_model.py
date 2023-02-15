from src.app.model import db
from src.app.model.enums import payment_type, provider_type


class BillTemplateModel(db.Model):  # type: ignore[name-defined]
    __tablename__ = "template"

    id_ = db.Column("id", db.Integer, primary_key=True)
    provider = db.Column(provider_type, nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    due_date = db.Column(db.Date, nullable=False)
    payment = db.Column(payment_type, nullable=False)
    biweekly = db.Column(db.Boolean, nullable=False, default=False)
