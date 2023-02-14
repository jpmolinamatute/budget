import uuid

from src.app.model import db
from src.app.model.payment_plan_model import PaymentPlanModel


class PaymentPlanControler:
    def save_bulk(self, payment_plans: list[PaymentPlanModel]) -> None:
        db.session.bulk_save_objects(payment_plans)
        db.session.commit()

    def update_payment_plan(self, payment_plan_id: uuid.UUID, amount: float) -> None:
        payment_plan = PaymentPlanModel.query.get(payment_plan_id)
        payment_plan.amount = amount
        db.session.commit()

    def process_payment_plan(self, budget_id: uuid.UUID, salary_id: uuid.UUID) -> list[PaymentPlanModel]:
        pass
