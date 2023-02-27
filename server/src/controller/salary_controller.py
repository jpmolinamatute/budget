import uuid
from datetime import datetime
from typing import TypedDict

from flask import current_app

from src.model import db
from src.model.salary_model import SalaryModel


class primitiveSalary(TypedDict):
    id_: uuid.UUID
    name: str
    amount: float
    date: datetime
    extra: float


class SalaryController:
    def __init__(self, budget_id: uuid.UUID) -> None:
        self.logger = current_app.logger
        self.budget_id = budget_id

    def update_salary_amount_extra(
        self,
        amount: float,
        salary_id: uuid.UUID,
        salary_type: str,
    ) -> None:
        salary = SalaryModel.query.filter_by(id_=salary_id).first()
        if salary_type == "amount":
            salary.amount = amount
        elif salary_type == "extra":
            salary.extra = amount
        db.session.commit()

    def get_salaries(self) -> list[primitiveSalary]:
        salaries_list: list[primitiveSalary] = []
        salaries = SalaryModel.query.filter_by(budget_id=self.budget_id).all()
        for salary in salaries:
            salaries_list.append(
                {
                    "id_": salary.id_,
                    "name": salary.name,
                    "amount": salary.amount,
                    "date": salary.date,
                    "extra": salary.extra,
                }
            )
        return salaries_list
