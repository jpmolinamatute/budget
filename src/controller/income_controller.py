import logging
import uuid

from datetime import datetime, timedelta
from typing import TypedDict

from sqlalchemy.orm import Session

from src.controller.budget_controller import BudgetController
from src.model.income_model import IncomeModel
from src.model.plan_model import PlanModel


class primitiveIncome(TypedDict):
    id_: uuid.UUID
    budget_id: uuid.UUID
    plan_id: uuid.UUID
    amount: float
    date: datetime
    income_type: str
    is_locked: bool


class IncomeController:
    def __init__(self, logger: logging.Logger, session: Session, budget: BudgetController) -> None:
        self.logger = logger
        self.session = session
        self.budget = budget
        self.cut_dates: list[datetime] = []

    def create(self, old_budget_id: uuid.UUID) -> None:
        self.logger.info("Creating new income")
        self.cut_dates = self.get_dates(old_budget_id)
        income_list = self.get_processed_income()
        self.save_bulk(income_list)

    def get_start_date(self, old_budget_id: uuid.UUID) -> datetime:
        self.logger.info("Getting start date")
        previous_plan = self.session.query(PlanModel).filter_by(budget_id=old_budget_id).first()
        if previous_plan is None:
            raise Exception("No previous plan")
        return previous_plan.end_date

    def get_dates(self, old_budget_id: uuid.UUID) -> list[datetime]:
        self.logger.info("Getting biweekly dates")
        start_date = self.get_start_date(old_budget_id)
        first_date = start_date + timedelta(days=14)
        last_date = first_date + timedelta(days=14)
        extra_date = last_date + timedelta(days=14)

        dates = [first_date, last_date]
        if extra_date.month == last_date.month:
            dates.append(extra_date)
        return dates

    def get_processed_income(self) -> list[IncomeModel]:
        self.logger.info("Getting processed income")
        income = []
        plan_id_list = self.get_plan_id_list()
        for a_date, plan_id in zip(self.cut_dates, plan_id_list):
            income.append(
                IncomeModel(
                    id_=uuid.uuid4(),
                    date=a_date,
                    amount=2920.92,
                    plan_id=plan_id,
                    budget_id=self.budget.budget_id,
                    income_type="salary",
                )
            )
        return income

    def get_plan_id_list(self) -> list[uuid.UUID]:
        self.logger.info("Getting plan id list")
        plan_id_list = []
        plans = self.session.query(PlanModel).filter_by(budget_id=self.budget.budget_id).all()
        for plan in plans:
            plan_id_list.append(plan.id_)
        return plan_id_list

    def save_bulk(self, bulk: list[IncomeModel]) -> None:
        self.logger.info("Saving bulk income data to database")
        self.session.bulk_save_objects(bulk)
        self.session.commit()

    def get_current_income(self) -> list[primitiveIncome]:
        income_list: list[primitiveIncome] = []
        incomes = self.session.query(IncomeModel).filter_by(budget_id=self.budget.budget_id).all()
        for income in incomes:
            income_list.append(
                {
                    "id_": income.id_,
                    "date": income.date,
                    "amount": income.amount,
                    "income_type": income.income_type,
                    "budget_id": income.budget_id,
                    "plan_id": income.plan_id,
                    "is_locked": income.is_locked,
                }
            )
        return income_list

    def add_income(self, amount: float, date: datetime, income_type: str) -> None:
        plan = self.session.query(PlanModel).filter_by(budget_id=self.budget.budget_id).first()
        if plan is None:
            raise Exception("No plan found")
        income = IncomeModel(
            id_=uuid.uuid4(),
            date=date,
            amount=amount,
            income_type=income_type,
            budget_id=self.budget.budget_id,
            plan_id=plan.id_,
            is_locked=False,
        )
        self.session.add(income)
        self.session.commit()

    def update_income_date(self, income_id: uuid.UUID, date: datetime) -> None:
        income = self.session.query(IncomeModel).filter_by(id_=income_id).first()
        if income is None:
            raise Exception("No income found")
        income.date = date
        self.session.commit()

    def update_income_amount(self, income_id: uuid.UUID, amount: float) -> None:
        income = self.session.query(IncomeModel).filter_by(id_=income_id).first()
        if income is None:
            raise Exception("No income found")
        income.amount = amount
        self.session.commit()

    def update_income_type(self, income_id: uuid.UUID, income_type: str) -> None:
        income = self.session.query(IncomeModel).filter_by(id_=income_id).first()
        if income is None:
            raise Exception("No income found")
        income.income_type = income_type
        self.session.commit()

    def mark_income_close(self, income_id: uuid.UUID) -> None:
        income = self.session.query(IncomeModel).filter_by(id_=income_id).first()
        if income is None:
            raise Exception("No income found")
        income.is_locked = True
        self.session.commit()

    def mark_income_reopen(self, income_id: uuid.UUID) -> None:
        income = self.session.query(IncomeModel).filter_by(id_=income_id).first()
        if income is None:
            raise Exception("No income found")
        income.is_locked = False
        self.session.commit()

    def delete_income(self, income_id: uuid.UUID) -> None:
        income = self.session.query(IncomeModel).filter_by(id_=income_id).first()
        if income is None:
            raise Exception("No income found")
        self.session.delete(income)
        self.session.commit()

    def is_income_locked(self, income_id: uuid.UUID) -> bool:
        income = self.session.query(IncomeModel).filter_by(id_=income_id).first()
        if income is None:
            raise Exception("No income found")
        return income.is_locked
