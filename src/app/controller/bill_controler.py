import uuid
from datetime import datetime
from typing import TypedDict

from sqlalchemy import desc

from src.app.controller import get_biweekly_dates
from src.app.model import db
from src.app.model.bill_model import BillModel
from src.app.model.bill_template_model import BillTemplateModel


class RawBill(TypedDict):
    provider: str
    amount: float
    due_date: int
    payment: str
    biweekly: bool


class BillControler:
    def save_bulk(self, bills: list[BillModel]) -> None:
        db.session.bulk_save_objects(bills)
        db.session.commit()

    def get_bills_from_template(self) -> list[RawBill]:
        template_list = BillTemplateModel.query.all()
        bill_list: list[RawBill] = []
        for bill in template_list:
            bill_list.append(
                {
                    "provider": bill.provider,
                    "amount": bill.amount,
                    "due_date": bill.due_date,
                    "payment": bill.payment,
                    "biweekly": bill.biweekly,
                }
            )
        return bill_list

    @staticmethod
    def get_dates(provider: str) -> list[datetime]:
        bill_filtered = db.session.query(BillModel.due_date).filter_by(provider=provider)
        bill = bill_filtered.order_by(desc(BillModel.due_date)).first()
        if not bill:
            raise Exception("No bill found")
        return get_biweekly_dates(bill[0])

    def process_bills(self, budget_id: uuid.UUID, month: int, year: int) -> list[BillModel]:
        bills = []
        for bill in self.get_bills_from_template():
            if bill["biweekly"]:
                date_list = self.get_dates(bill["provider"])
                for a_date in date_list:
                    bills.append(
                        BillModel(
                            id_=uuid.uuid4(),
                            budget_id=budget_id,
                            provider=bill["provider"],
                            amount=bill["amount"],
                            due_date=a_date,
                            payment=bill["payment"],
                        )
                    )
            else:
                due_date = datetime(year, month, bill["due_date"]) if bill["due_date"] else None
                bills.append(
                    BillModel(
                        id_=uuid.uuid4(),
                        budget_id=budget_id,
                        provider=bill["provider"],
                        amount=bill["amount"],
                        due_date=due_date,
                        payment=bill["payment"],
                    )
                )
        return bills

    @staticmethod
    def update_salary(bill_id: uuid.UUID, amount: float) -> None:
        bill = BillModel.query.get(bill_id)
        bill.amount = amount
        db.session.commit()
