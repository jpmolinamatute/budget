import uuid
from typing import Optional

from src.model import db
from src.model.budget_model import BudgetModel


class BudgetController:
    def close_budget(self, budget_id: uuid.UUID) -> None:
        budget = BudgetModel.query.filter_by(id_=budget_id).first()
        budget.is_current = False
        db.session.commit()

    def create_budget(self, month: int, year: int) -> Optional[uuid.UUID]:
        budget_id = uuid.uuid4()
        budget = BudgetModel(id_=budget_id, month=month, year=year, is_current=True)
        db.session.add(budget)
        db.session.commit()
        return budget_id

    def get_current_budget(self) -> Optional[uuid.UUID]:
        # use db.session to query all budget with is_current = True.
        # If there is any, return its id, else return None
        budget_id = None
        budget = BudgetModel.query.filter_by(is_current=True).first()
        if budget:
            budget_id = budget.id_
        return budget_id
