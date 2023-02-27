import uuid
from typing import TypedDict

from flask import current_app

from src.model import db
from src.model.payment_plan_model import PaymentPlanModel


class primitivePaymentPlan(TypedDict):
    id_: uuid.UUID
    payment: str
    amount: float
    is_closed: bool


class PaymentPlanController:
    def __init__(self, budget_id: uuid.UUID) -> None:
        self.logger = current_app.logger
        self.budget_id = budget_id

    def update_payment_plan_amount(self, amount: float, payment_plan_id: uuid.UUID) -> None:
        payment_plan = PaymentPlanModel.query.filter_by(id_=payment_plan_id).first()
        payment_plan.amount = amount
        db.session.commit()

    def mark_payment_plan_closed(self, payment_plan_id: uuid.UUID) -> None:
        payment_plan = PaymentPlanModel.query.filter_by(id_=payment_plan_id).first()
        payment_plan.is_closed = True
        db.session.commit()

    def get_payment_plans(self) -> list[primitivePaymentPlan]:
        payment_plan_list: list[primitivePaymentPlan] = []
        payment_plans = PaymentPlanModel.query.filter_by(budget_id=self.budget_id).all()
        for payment_plan in payment_plans:
            payment_plan_list.append(
                {
                    "id_": payment_plan.id_,
                    "payment": payment_plan.payment,
                    "amount": payment_plan.amount,
                    "is_closed": payment_plan.is_closed,
                }
            )
        return payment_plan_list
