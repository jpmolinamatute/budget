import uuid

from datetime import datetime, timedelta
from typing import Optional, TypedDict, Union

from flask import current_app
from sqlalchemy import desc

from src.model import db
from src.model.bill_model import BillModel
from src.model.bill_template_model import BillTemplateModel
from src.model.budget_model import BudgetModel
from src.model.income_model import IncomeModel
from src.model.payment_plan_model import PaymentPlanModel


class RawBill(TypedDict):
    provider: str
    amount: float
    due_date: int
    payment: str
    biweekly: bool


class Plan(TypedDict):
    income_id: uuid.UUID
    item: dict[str, float]


BULK_TYPE_LIST = list[Union[IncomeModel, BillModel, PaymentPlanModel]]


class PrimitiveBudget(TypedDict):
    month: int
    year: int
    cut_dates: list[datetime]
    start_date: datetime
    end_date: datetime


class CompleteBudgetControler:
    def __init__(self) -> None:
        self.logger = current_app.logger
        self.year = 0
        self.month = 0
        self.start_date: Optional[datetime] = None
        self.end_date: Optional[datetime] = None
        self.cut_dates: list[datetime] = []
        self.budget_id: Optional[uuid.UUID] = None

    def new_budget(self, old_budget_id: uuid.UUID) -> None:
        self.logger.info("Creating new budget")
        old_budget = self.close_budget(old_budget_id)
        new_info = self.get_next_buget_info(old_budget)
        self.year = new_info["year"]
        self.month = new_info["month"]
        self.start_date = new_info["start_date"]
        self.end_date = new_info["end_date"]
        self.cut_dates = new_info["cut_dates"]
        self.budget_id = self.create_budget()

    def get_current_budget_id(self) -> Optional[uuid.UUID]:
        self.logger.info("Getting current budget")
        # use db.session to query all budget with is_current = True.
        # If there is any, return its id, else return None
        budget_id = None
        budget = BudgetModel.query.filter_by(is_current=True).first()
        if budget:
            budget_id = budget.id_
        return budget_id

    def create_budget(self) -> Optional[uuid.UUID]:
        self.logger.info("Creating new budget")
        budget_id = uuid.uuid4()
        budget = BudgetModel(
            id_=budget_id,
            month=self.month,
            year=self.year,
            start_date=self.start_date,
            end_date=self.end_date,
            is_current=True,
        )
        db.session.add(budget)
        db.session.commit()
        return budget_id

    def get_next_buget_info(self, old_budget: BudgetModel) -> PrimitiveBudget:
        old_date = datetime(old_budget.year, old_budget.month, 1)
        new_date = old_date + timedelta(days=31)
        cut_dates = self.get_biweekly_dates(old_budget.end_date)
        return {
            "month": new_date.month,
            "year": new_date.year,
            "cut_dates": cut_dates,
            "start_date": old_budget.end_date,
            "end_date": cut_dates[-1],
        }

    def close_budget(self, old_budget_id: uuid.UUID) -> BudgetModel:
        self.logger.info("Closing old budget")
        budget = BillModel.query.filter_by(budget_id=old_budget_id, is_paid=False).all()
        if len(budget) > 0:
            self.logger.error("Cannot close budget")
        budget = BudgetModel.query.filter_by(id_=old_budget_id).first()
        budget.is_current = False
        db.session.commit()
        return budget

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

    def get_biweekly_dates(self, start_date: datetime) -> list[datetime]:
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
        bill = bill_filtered.order_by(desc(BillModel.due_date)).first()
        if not bill:
            raise Exception("No bill found")
        return self.get_biweekly_dates(bill[0])

    def process_bills(self) -> None:
        self.logger.info("Processing bills")
        bill_list = self.get_processed_bills()
        self.save_bulk(bill_list)

    def get_processed_bills(self) -> list[BillModel]:
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
                    due_date = datetime(self.year, self.month, bill["due_date"])
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

    def save_bulk(self, bulk: BULK_TYPE_LIST) -> None:
        self.logger.info("Saving bulk data to database")
        db.session.bulk_save_objects(bulk)
        db.session.commit()

    def process_income(self) -> None:
        self.logger.info("Processing income")
        income_list = self.get_processed_income()
        self.save_bulk(income_list)

    def get_processed_income(self) -> list[IncomeModel]:
        self.logger.info("Getting processed income")
        income = []
        for a_date in self.cut_dates:
            income.append(
                IncomeModel(
                    id_=uuid.uuid4(),
                    date=a_date,
                    amount=2920.92,
                    budget_id=self.budget_id,
                    income_type="salary",
                )
            )
        return income

    def get_month_bill_plan(self) -> dict[str, float]:
        self.logger.info("Getting bills for month plan")
        total_per_payment: dict[str, float] = {}
        bills = BillModel.query.filter_by(budget_id=self.budget_id).all()
        for bill in bills:
            if bill.payment in total_per_payment:
                total_per_payment[bill.payment] += bill.amount
            else:
                total_per_payment[bill.payment] = bill.amount
        return total_per_payment

    def get_biweek_bill_plan(self) -> dict[str, float]:
        self.logger.info("Getting bills for biweekly plan")
        month_plan = self.get_month_bill_plan()
        number_of_biweeks = len(self.cut_dates)
        total_per_payment_biweekly: dict[str, float] = {}

        for payment, amount in month_plan.items():
            total_per_payment_biweekly[payment] = amount / number_of_biweeks
        return total_per_payment_biweekly

    def get_income_id_list(self) -> list[uuid.UUID]:
        self.logger.info("Getting income id list")
        income_id_list = []
        for income in IncomeModel.query.filter_by(budget_id=self.budget_id).all():
            income_id_list.append(income.id_)
        return income_id_list

    def get_payment_plan(self) -> list[Plan]:
        self.logger.info("Getting payment plan")
        biweek_plan = []
        item = self.get_biweek_bill_plan()
        income_id_list = self.get_income_id_list()
        for income_id in income_id_list:
            biweek_plan1: Plan = {
                "income_id": income_id,
                "item": item,
            }
            biweek_plan.append(biweek_plan1)
        return biweek_plan

    def process_payment_plan(self) -> None:
        self.logger.info("Processing payment plan")
        payment_plan = self.get_payment_plan()
        payment_plan_list = self.get_processed_payment_plan(payment_plan)
        self.save_bulk(payment_plan_list)

    def get_processed_payment_plan(self, payment_plan: list[Plan]) -> list[PaymentPlanModel]:
        self.logger.info("Getting processed payment plan")
        payment_plan_list: list[PaymentPlanModel] = []
        for plan in payment_plan:
            for payment, amount in plan["item"].items():
                payment_plan = PaymentPlanModel(
                    id_=uuid.uuid4(),
                    budget_id=self.budget_id,
                    income_id=plan["income_id"],
                    amount=amount,
                    payment=payment,
                )
                payment_plan_list.append(payment_plan)
        return payment_plan_list

    def process(self) -> None:
        self.logger.info("Creating a whole new budget with bills and income")
        self.process_bills()
        self.process_income()
        self.process_payment_plan()
