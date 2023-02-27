import uuid

from datetime import datetime
from typing import TypedDict

from flask import current_app

from src.model import db
from src.model.enums import IncomeType
from src.model.income_model import IncomeModel


class primitiveIncome(TypedDict):
    id_: uuid.UUID
    name: str
    amount: float
    date: datetime
    income_type: IncomeType


class IncomeController:
    def __init__(self, budget_id: uuid.UUID) -> None:
        self.logger = current_app.logger
        self.budget_id = budget_id

    def update_income_amount(self, amount: float, income_id: uuid.UUID) -> None:
        self.logger.info(f"Updating income amount to {amount} for income {income_id}")
        income = IncomeModel.query.filter_by(id_=income_id).first()
        income.amount = amount
        db.session.commit()

    def get_salaries(self) -> list[primitiveIncome]:
        self.logger.info(f"Getting salaries for budget {self.budget_id}")
        salaries_list: list[primitiveIncome] = []
        salaries = IncomeModel.query.filter_by(budget_id=self.budget_id).all()
        for income in salaries:
            salaries_list.append(
                {
                    "id_": income.id_,
                    "name": income.name,
                    "amount": income.amount,
                    "date": income.date,
                    "income_type": income.income_type,
                }
            )
        return salaries_list

    def add_other_income(self, name: str, amount: float, date: datetime) -> None:
        self.logger.info(f"Adding other income {name} for budget {self.budget_id}")
        income = IncomeModel(
            name=name,
            amount=amount,
            date=date,
            income_type="other",
            budget_id=self.budget_id,
        )
        db.session.add(income)
        db.session.commit()

    def delete_other_income(self, income_id: uuid.UUID) -> None:
        self.logger.info(f"Deleting other income {income_id}")
        income = IncomeModel.query.filter_by(id_=income_id).first()
        db.session.delete(income)
        db.session.commit()
