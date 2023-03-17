import logging
import uuid

from datetime import datetime, timedelta
from typing import TypedDict

from sqlalchemy.orm import Session

from src.controller.budget_controller import BudgetController
from src.model.bill_model import BillModel
from src.model.reference_model import BillTemplateModel


class RawBill(TypedDict):
    provider_type: str
    amount: float
    due_date: int
    payment_type: str
    biweekly: bool


class primitiveBill(TypedDict):
    id_: uuid.UUID
    provider_type: str
    amount: float
    due_date: datetime
    payment_type: str
    is_locked: bool


class BillController:
    def __init__(self, logger: logging.Logger, session: Session, budget: BudgetController) -> None:
        self.session = session
        self.logger = logger
        self.budget = budget

    def create(self) -> None:
        self.logger.info("Creating new bills")
        bill_list = self.get_processed_bills()
        self.save_bulk(bill_list)

    def get_bills_from_template(self) -> list[RawBill]:
        self.logger.info("Getting recurrent bills from template")
        template_list = self.session.query(BillTemplateModel).all()
        bill_list: list[RawBill] = []
        for bill in template_list:
            bill_list.append(
                {
                    "provider_type": bill.provider_type,
                    "amount": bill.amount,
                    "due_date": bill.due_date,
                    "payment_type": bill.payment_type,
                    "biweekly": bill.biweekly,
                }
            )
        return bill_list

    def get_processed_bills(self) -> list[BillModel]:
        self.logger.info("Getting processed bills")
        bills = []
        for bill in self.get_bills_from_template():
            if bill["biweekly"]:
                date_list = self.get_bill_dates(bill["provider_type"])
                for a_date in date_list:
                    bills.append(
                        BillModel(
                            id_=uuid.uuid4(),
                            budget_id=self.budget.budget_id,
                            provider_type=bill["provider_type"],
                            amount=bill["amount"],
                            due_date=a_date,
                            payment_type=bill["payment_type"],
                        )
                    )
            else:
                if bill["due_date"]:
                    due_date = datetime(self.budget.year, self.budget.month, bill["due_date"])
                else:
                    due_date = None
                bills.append(
                    BillModel(
                        id_=uuid.uuid4(),
                        budget_id=self.budget.budget_id,
                        provider_type=bill["provider_type"],
                        amount=bill["amount"],
                        due_date=due_date,
                        payment_type=bill["payment_type"],
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

    def get_bill_dates(self, provider_type: str) -> list[datetime]:
        self.logger.info("Getting bill dates for a given provider based on last bill")
        bill_filtered = self.session.query(BillModel.due_date).filter_by(
            provider_type=provider_type
        )
        bill = bill_filtered.order_by(BillModel.due_date.desc()).first()
        if bill is None:
            raise Exception("No bill found")
        return self.get_dates(bill[0])

    def save_bulk(self, bulk: list[BillModel]) -> None:
        self.logger.info("Saving bulk bill data to database")
        self.session.bulk_save_objects(bulk)
        self.session.commit()

    def get_current_bill(self) -> list[primitiveBill]:
        bills = self.session.query(BillModel).filter_by(budget_id=self.budget.budget_id).all()
        bill_list: list[primitiveBill] = []
        for bill in bills:
            bill_list.append(
                {
                    "id_": bill.id_,
                    "provider_type": bill.provider_type,
                    "amount": bill.amount,
                    "due_date": bill.due_date,
                    "payment_type": bill.payment_type,
                    "is_locked": bill.is_locked,
                }
            )
        return bill_list

    def mark_bill_paid(self, bill_id: uuid.UUID) -> None:
        bill = self.session.query(BillModel).filter_by(id_=bill_id).first()
        if bill is None:
            raise Exception("No bill found")
        bill.is_locked = True
        self.session.commit()

    def mark_bill_unpaid(self, bill_id: uuid.UUID) -> None:
        bill = self.session.query(BillModel).filter_by(id_=bill_id).first()
        if bill is None:
            raise Exception("No bill found")
        bill.is_locked = False
        self.session.commit()

    def update_bill_amount(self, bill_id: uuid.UUID, amount: float) -> None:
        bill = self.session.query(BillModel).filter_by(id_=bill_id).first()
        if bill is None:
            raise Exception("No bill found")
        bill.amount = amount
        self.session.commit()

    def update_bill_due_date(self, bill_id: uuid.UUID, date: datetime) -> None:
        bill = self.session.query(BillModel).filter_by(id_=bill_id).first()
        if bill is None:
            raise Exception("No bill found")
        bill.due_date = date
        self.session.commit()
