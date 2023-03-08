import logging
import uuid

from datetime import datetime, timedelta
from typing import TypedDict

from src.controller.budget_controller import BudgetController
from src.model import db
from src.model.enums import IncomeType
from src.model.income_model import IncomeModel
from src.model.plan_model import PlanModel


class primitiveIncome(TypedDict):
    id_: uuid.UUID
    budget_id: uuid.UUID
    plan_id: uuid.UUID
    amount: float
    date: datetime
    income_type: IncomeType
    is_locked: bool


class IncomeController:
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        self.budget_id = BudgetController.get_current_budget_id()
        self.cut_dates: list[datetime] = []

    def create(self, old_budget_id: uuid.UUID) -> None:
        self.logger.info("Creating new income")
        self.cut_dates = self.get_dates(old_budget_id)
        income_list = self.get_processed_income()
        self.save_bulk(income_list)

    def get_start_date(self, old_budget_id: uuid.UUID) -> datetime:
        self.logger.info("Getting start date")
        previous_plan = PlanModel.query.filter_by(budget_id=old_budget_id).first()
        if not previous_plan:
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
                    budget_id=self.budget_id,
                    income_type="salary",
                )
            )
        return income

    def get_plan_id_list(self) -> list[uuid.UUID]:
        self.logger.info("Getting plan id list")
        plan_id_list = []
        for plan in PlanModel.query.filter_by(budget_id=self.budget_id).all():
            plan_id_list.append(plan.id_)
        return plan_id_list

    def save_bulk(self, bulk: list[IncomeModel]) -> None:
        self.logger.info("Saving bulk income data to database")
        db.session.bulk_save_objects(bulk)
        db.session.commit()

    @staticmethod
    def get_current_income() -> list[primitiveIncome]:
        budget_id = BudgetController.get_current_budget_id()
        income_list: list[primitiveIncome] = []
        incomes = IncomeModel.query.filter_by(budget_id=budget_id).all()
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

    @staticmethod
    def add_income(amount: float, date: datetime, income_type: IncomeType) -> None:
        budget_id = BudgetController.get_current_budget_id()
        plan_id = PlanModel.query.filter_by(budget_id=budget_id).first().id_
        income = IncomeModel(
            id_=uuid.uuid4(),
            date=date,
            amount=amount,
            income_type=income_type,
            budget_id=budget_id,
            plan_id=plan_id,
            is_locked=False,
        )
        db.session.add(income)
        db.session.commit()

    @staticmethod
    def update_income_date(income_id: uuid.UUID, date: datetime) -> None:
        income = IncomeModel.query.filter_by(id_=income_id).first()
        income.date = date
        db.session.commit()

    @staticmethod
    def update_income_amount(income_id: uuid.UUID, amount: float) -> None:
        income = IncomeModel.query.filter_by(id_=income_id).first()
        income.amount = amount
        db.session.commit()

    @staticmethod
    def update_income_type(income_id: uuid.UUID, income_type: IncomeType) -> None:
        income = IncomeModel.query.filter_by(id_=income_id).first()
        income.income_type = income_type
        db.session.commit()

    @staticmethod
    def mark_income_close(income_id: uuid.UUID) -> None:
        income = IncomeModel.query.filter_by(id_=income_id).first()
        income.is_locked = True
        db.session.commit()

    @staticmethod
    def mark_income_reopen(income_id: uuid.UUID) -> None:
        income = IncomeModel.query.filter_by(id_=income_id).first()
        income.is_locked = False
        db.session.commit()

    @staticmethod
    def delete_income(income_id: uuid.UUID) -> None:
        income = IncomeModel.query.filter_by(id_=income_id).first()
        db.session.delete(income)
        db.session.commit()
