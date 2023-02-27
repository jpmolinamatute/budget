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
        income = IncomeModel.query.filter_by(id_=income_id).first()
        income.amount = amount
        db.session.commit()

    def get_salaries(self) -> list[primitiveIncome]:
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
