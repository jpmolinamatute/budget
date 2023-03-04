import logging
import uuid

from datetime import datetime, timedelta
from typing import TypedDict

from src.controller.budget_controller import BudgetController
from src.model import db
from src.model.bill_model import BillModel
from src.model.bill_template_model import BillTemplateModel


class RawBill(TypedDict):
    provider: str
    amount: float
    due_date: int
    payment: str
    biweekly: bool


class primitiveBill(TypedDict):
    id_: uuid.UUID
    provider: str
    amount: float
    due_date: datetime
    payment: str
    is_locked: bool


class BillController:
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        self.budget_id: uuid.UUID

    def create(self) -> None:
        self.logger.info("Creating new bills")
        current_budget = BudgetController.get_current_budget()
        self.budget_id = current_budget["id_"]
        bill_list = self.get_processed_bills(current_budget["year"], current_budget["month"])
        self.save_bulk(bill_list)

    def get_bills_from_template(self) -> list[RawBill]:
        self.logger.info("Getting recurrent bills from template")
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

    def get_processed_bills(self, year: int, month: int) -> list[BillModel]:
        self.logger.info("Getting processed bills")
        bills = []
        for bill in self.get_bills_from_template():
            if bill["biweekly"]:
                date_list = self.get_bill_dates(bill["provider"])
                for a_date in date_list:
                    bills.append(
                        BillModel(
                            id_=uuid.uuid4(),
                            budget_id=self.budget_id,
                            provider=bill["provider"],
                            amount=bill["amount"],
                            due_date=a_date,
                            payment=bill["payment"],
                        )
                    )
            else:
                if bill["due_date"]:
                    due_date = datetime(year, month, bill["due_date"])
                else:
                    due_date = None
                bills.append(
                    BillModel(
                        id_=uuid.uuid4(),
                        budget_id=self.budget_id,
                        provider=bill["provider"],
                        amount=bill["amount"],
                        due_date=due_date,
                        payment=bill["payment"],
                    )
                )
        return bills

    def get_dates(self, start_date: datetime) -> list[datetime]:
        self.logger.info("Getting biweekly dates")
        first_date = start_date + timedelta(days=14)
        last_date = first_date + timedelta(days=14)
        extra_date = last_date + timedelta(days=14)

        dates = [first_date, last_date]
        if extra_date.month == last_date.month:
            dates.append(extra_date)
        return dates

    def get_bill_dates(self, provider: str) -> list[datetime]:
        self.logger.info("Getting bill dates for a given provider based on last bill")
        bill_filtered = db.session.query(BillModel.due_date).filter_by(provider=provider)
        bill = bill_filtered.order_by(BillModel.due_date.desc()).first()
        if not bill:
            raise Exception("No bill found")
        return self.get_dates(bill[0])

    def save_bulk(self, bulk: list[BillModel]) -> None:
        self.logger.info("Saving bulk bill data to database")
        db.session.bulk_save_objects(bulk)
        db.session.commit()

    @staticmethod
    def get_bills() -> list[primitiveBill]:
        budget_id = BudgetController.get_current_budget_id()
        bills = BillModel.query.filter_by(budget_id=budget_id).all()
        bill_list: list[primitiveBill] = []
        for bill in bills:
            bill_list.append(
                {
                    "id_": bill.id_,
                    "provider": bill.provider,
                    "amount": bill.amount,
                    "due_date": bill.due_date,
                    "payment": bill.payment,
                    "is_locked": bill.is_locked,
                }
            )
        return bills

    @staticmethod
    def mark_bill_paid(bill_id: uuid.UUID) -> None:
        bill = BillModel.query.filter_by(id_=bill_id).first()
        bill.is_locked = True
        db.session.commit()

    @staticmethod
    def update_bill_amount(amount: float, bill_id: uuid.UUID) -> None:
        bill = BillModel.query.filter_by(id_=bill_id).first()
        bill.amount = amount
        db.session.commit()
