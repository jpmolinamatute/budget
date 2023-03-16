import logging
import uuid

from datetime import datetime, timedelta
from typing import Optional, TypedDict

from sqlalchemy.orm import Session

from src.model.bill_model import BillModel
from src.model.budget_model import BudgetModel


class BudgetController:
    def __init__(
        self, logger: logging.Logger, session: Session, budget_id: Optional[uuid.UUID] = None
    ) -> None:
        self.logger = logger
        self.session = session
        budget = self.get_current_budget(budget_id)
        self.budget_id = budget.id_
        self.month = budget.month
        self.year = budget.year
        self.is_locked = budget.is_locked

    def close_budget(self) -> BudgetModel:
        self.logger.info("Closing old budget")
        bills = (
            self.session.query(BillModel).filter_by(budget_id=self.budget_id, is_locked=False).all()
        )
        if len(bills) > 0:
            raise Exception("ERROR: Cannot close budget. There bills to be paid")
        budget = self.session.query(BudgetModel).filter_by(id_=self.budget_id).first()
        if budget is None:
            raise Exception("Budget not found")
        budget.is_locked = True
        self.session.commit()
        return budget

    def create(self, old_budget: BudgetModel) -> uuid.UUID:
        self.logger.info("Creating new budget")
        old_date = datetime(old_budget.year, old_budget.month, 1)
        new_date = old_date + timedelta(days=31)
        self.budget_id = uuid.uuid4()
        self.month = new_date.month
        self.year = new_date.year
        budget = BudgetModel(
            id_=self.budget_id,
            month=self.month,
            year=self.year,
            is_locked=False,
        )
        self.session.add(budget)
        self.session.commit()
        return self.budget_id

    def get_current_budget(self, budget_id: Optional[uuid.UUID] = None) -> BudgetModel:
        if budget_id:
            current_budget = self.session.query(BudgetModel).filter_by(id_=budget_id).first()
        else:
            current_budget = self.session.query(BudgetModel).filter_by(is_locked=False).first()

        if current_budget is None:
            raise Exception("Budget not found")

        return current_budget
