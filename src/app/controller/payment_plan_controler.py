from src.app.model import db
from src.app.model.payment_plan_model import PaymentPlanModel


class PaymentPlanControler:
    def save_bulk(self, payment_plans: list[PaymentPlanModel]) -> None:
        db.session.bulk_save_objects(payment_plans)
        db.session.commit()
