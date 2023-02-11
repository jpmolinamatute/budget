import uuid
from typing import Optional
from src.app.model import db
from src.app.model.budget_model import BudgetModel


class BudgetController:
    def close_budget(self, budget_id: uuid.UUID) -> None:
        budget = BudgetModel.query.filter_by(id_=budget_id).first()
        budget.is_current = False
        db.session.commit()

    def are_budget_closed(self) -> bool:
        # use db.session to query all budget with is_current = True.
        # If there is any, return False, else return True
        all_budgets = BudgetModel.query.filter_by(is_current=True).all()
        return len(all_budgets) == 0

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
        all_budgets = BudgetModel.query.filter_by(is_current=True).all()
        if len(all_budgets) == 1:
            budget_id = all_budgets[0].id_
        return budget_id

    def open_budget(self, month: int, year: int) -> Optional[uuid.UUID]:
        # use db.session to query all budget with is_current = True.
        # If there is any, return None, else create a new budget and return its id
        budget_id = None
        if self.are_budget_closed():
            budget_id = self.create_budget(month, year)
        else:
            budget_id = self.get_current_budget()
        return budget_id
