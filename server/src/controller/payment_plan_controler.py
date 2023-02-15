import uuid
from typing import TypedDict

from src.model import db
from src.model.payment_plan_model import PaymentPlanModel


class Plan(TypedDict):
    budget_id: uuid.UUID
    salary_id: uuid.UUID
    item: dict[str, float]


class PaymentPlanControler:
    def save_bulk(self, payment_plans: list[PaymentPlanModel]) -> None:
        db.session.bulk_save_objects(payment_plans)
        db.session.commit()

    def update_payment_plan(self, payment_plan_id: uuid.UUID, amount: float) -> None:
        payment_plan = PaymentPlanModel.query.get(payment_plan_id)
        payment_plan.amount = amount
        db.session.commit()

    def process_payment_plan(self, payment_plan: list[Plan]) -> list[PaymentPlanModel]:
        payment_plan_list: list[PaymentPlanModel] = []
        for plan in payment_plan:
            for payment, amount in plan["item"].items():
                payment_plan = PaymentPlanModel(
                    id_=uuid.uuid4(),
                    budget_id=plan["budget_id"],
                    salary_id=plan["salary_id"],
                    amount=amount,
                    payment=payment,
                )
                payment_plan_list.append(payment_plan)
        return payment_plan_list
