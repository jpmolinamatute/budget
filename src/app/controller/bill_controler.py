import uuid
from datetime import datetime
from typing import TypedDict

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

    def get_bills_biweekly_dates(self, month: int, year: int) -> tuple[datetime, datetime]:
        first_date = datetime(year, month, 1)
        second_date = datetime(year, month, 15)
        return first_date, second_date

    def process_bills(self, budget_id: uuid.UUID, month: int, year: int) -> list[BillModel]:
        bills = []
        for bill in self.get_bills_from_template():
            if bill["biweekly"]:
                due_date_1, due_date_2 = self.get_bills_biweekly_dates(month, year)
                bills.append(
                    BillModel(
                        id_=uuid.uuid4(),
                        budget_id=budget_id,
                        provider=bill["provider"],
                        amount=bill["amount"],
                        due_date=due_date_1,
                        payment=bill["payment"],
                    )
                )

                bills.append(
                    BillModel(
                        id_=uuid.uuid4(),
                        budget_id=budget_id,
                        provider=bill["provider"],
                        amount=bill["amount"],
                        due_date=due_date_2,
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
