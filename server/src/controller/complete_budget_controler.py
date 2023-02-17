import uuid
from datetime import datetime, timedelta
from typing import Optional, TypedDict, Union

from sqlalchemy import desc

from src.model import db
from src.model.bill_model import BillModel
from src.model.bill_template_model import BillTemplateModel
from src.model.budget_model import BudgetModel
from src.model.payment_plan_model import PaymentPlanModel
from src.model.salary_model import SalaryModel


class RawBill(TypedDict):
    provider: str
    amount: float
    due_date: int
    payment: str
    biweekly: bool


class Plan(TypedDict):
    salary_id: uuid.UUID
    item: dict[str, float]


BULK_TYPE_LIST = list[Union[SalaryModel, BillModel, PaymentPlanModel]]


class CompleteBudgetControler:
    def __init__(self, month: int, year: int, old_budget: Optional[uuid.UUID] = None):
        current_date = datetime.now()
        if old_budget:
            self.close_budget(old_budget)

        if month < current_date.month or month > 12:
            raise Exception("Invalid month")

        if year < current_date.year:
            raise Exception("Invalid year")

        self.year = year
        self.month = month
        self.budget_id = self.get_current_budget()
        if self.budget_id is None:
            self.budget_id = self.create_budget()

    @staticmethod
    def get_current_budget() -> Optional[uuid.UUID]:
        # use db.session to query all budget with is_current = True.
        # If there is any, return its id, else return None
        budget_id = None
        budget = BudgetModel.query.filter_by(is_current=True).first()
        if budget:
            budget_id = budget.id_
        return budget_id

    def create_budget(self) -> Optional[uuid.UUID]:
        budget_id = uuid.uuid4()
        budget = BudgetModel(id_=budget_id, month=self.month, year=self.year, is_current=True)
        db.session.add(budget)
        db.session.commit()
        return budget_id

    @staticmethod
    def can_close_budget(old_budget: uuid.UUID) -> bool:
        budget = BillModel.query.filter_by(budget_id=old_budget, is_paid=False).all()
        return len(budget) == 0

    def close_budget(self, old_budget: uuid.UUID) -> None:
        if not self.can_close_budget(old_budget):
            raise Exception("Cannot close budget")
        budget = BudgetModel.query.filter_by(id_=old_budget).first()
        budget.is_current = False
        db.session.commit()

    @staticmethod
    def get_bills_from_template() -> list[RawBill]:
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
    def get_biweekly_dates(start_date: datetime) -> list[datetime]:
        first_date = start_date + timedelta(days=14)
        last_date = first_date + timedelta(days=14)
        extra_date = last_date + timedelta(days=14)

        dates = [first_date, last_date]
        if extra_date.month == last_date.month:
            dates.append(extra_date)
        return dates

    def get_bill_dates(self, provider: str) -> list[datetime]:
        bill_filtered = db.session.query(BillModel.due_date).filter_by(provider=provider)
        bill = bill_filtered.order_by(desc(BillModel.due_date)).first()
        if not bill:
            raise Exception("No bill found")
        return self.get_biweekly_dates(bill[0])

    def process_bills(self) -> None:
        bill_list = self.get_processed_bills()
        self.save_bulk(bill_list)

    def get_processed_bills(self) -> list[BillModel]:
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

    @staticmethod
    def save_bulk(bulk: BULK_TYPE_LIST) -> None:
        db.session.bulk_save_objects(bulk)
        db.session.commit()

    def get_salary_dates(self) -> list[datetime]:
        salary = db.session.query(SalaryModel.date).order_by(desc(SalaryModel.date)).first()
        if not salary:
            raise Exception("No salary found")
        return self.get_biweekly_dates(salary[0])

    def process_salaries(self) -> list[Plan]:
        salary_list = self.get_processed_salaries()
        self.save_bulk(salary_list)
        return self.get_payment_plan(salary_list)

    def get_processed_salaries(self) -> list[SalaryModel]:
        salaries = []
        for a_date in self.get_salary_dates():
            salaries.append(
                SalaryModel(
                    id_=uuid.uuid4(),
                    date=a_date,
                    amount=2920.92,
                    budget_id=self.budget_id,
                )
            )
        return salaries

    def get_month_bill_pan(self) -> dict[str, float]:
        total_per_payment: dict[str, float] = {}
        bills = BillModel.query.filter_by(budget_id=self.budget_id).all()
        for bill in bills:
            if bill.payment in total_per_payment:
                total_per_payment[bill.payment] += bill.amount
            else:
                total_per_payment[bill.payment] = bill.amount
        return total_per_payment

    def get_biweek_bill_plan(self, number_of_biweeks: int) -> dict[str, float]:
        month_plan = self.get_month_bill_pan()
        total_per_payment_biweekly: dict[str, float] = {}

        for payment, amount in month_plan.items():
            total_per_payment_biweekly[payment] = amount / number_of_biweeks
        return total_per_payment_biweekly

    def get_payment_plan(self, salary_list: list[SalaryModel]) -> list[Plan]:
        number_of_biweeks = len(salary_list)
        biweek_plan = []
        item = self.get_biweek_bill_plan(number_of_biweeks)
        for salary in salary_list:
            biweek_plan1: Plan = {
                "salary_id": salary.id_,
                "item": item,
            }
            biweek_plan.append(biweek_plan1)
        return biweek_plan

    def process_payment_plan(self, payment_plan: list[Plan]) -> None:
        payment_plan_list = self.get_processed_payment_plan(payment_plan)
        self.save_bulk(payment_plan_list)

    def get_processed_payment_plan(self, payment_plan: list[Plan]) -> list[PaymentPlanModel]:
        payment_plan_list: list[PaymentPlanModel] = []
        for plan in payment_plan:
            for payment, amount in plan["item"].items():
                payment_plan = PaymentPlanModel(
                    id_=uuid.uuid4(),
                    budget_id=self.budget_id,
                    salary_id=plan["salary_id"],
                    amount=amount,
                    payment=payment,
                )
                payment_plan_list.append(payment_plan)
        return payment_plan_list
