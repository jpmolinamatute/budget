import uuid

from datetime import datetime
from typing import TypedDict

from flask import current_app

from src.model import db
from src.model.bill_model import BillModel


class primitiveBill(TypedDict):
    id_: uuid.UUID
    provider: str
    amount: float
    due_date: datetime
    payment: str
    is_paid: bool


class BillController:
    def __init__(self, budget_id: uuid.UUID) -> None:
        self.logger = current_app.logger
        self.budget_id = budget_id

    def get_bills(self) -> list[primitiveBill]:
        bills = BillModel.query.filter_by(budget_id=self.budget_id).all()
        bill_list: list[primitiveBill] = []
        for bill in bills:
            bill_list.append(
                {
                    "id_": bill.id_,
                    "provider": bill.provider,
                    "amount": bill.amount,
                    "due_date": bill.due_date,
                    "payment": bill.payment,
                    "is_paid": bill.is_paid,
                }
            )
        return bills

    def mark_bill_paid(self, bill_id: uuid.UUID) -> None:
        bill = BillModel.query.filter_by(id_=bill_id).first()
        bill.is_paid = True
        db.session.commit()

    def update_bill_amount(self, amount: float, bill_id: uuid.UUID) -> None:
        bill = BillModel.query.filter_by(id_=bill_id).first()
        bill.amount = amount
        db.session.commit()
