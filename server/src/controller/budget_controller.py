import logging
import uuid

from datetime import datetime, timedelta

from src.model import db
from src.model.bill_model import BillModel
from src.model.budget_model import BudgetModel


class BudgetController:
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger

    def close_budget(self, old_budget_id: uuid.UUID) -> BudgetModel:
        self.logger.info("Closing old budget")
        budget = BillModel.query.filter_by(budget_id=old_budget_id, is_paid=False).all()
        if len(budget) > 0:
            raise Exception("Cannot close budget")
        budget = BudgetModel.query.filter_by(id_=old_budget_id).first()
        budget.is_current = False
        db.session.commit()
        return budget

    def create(self, old_budget_id: uuid.UUID) -> uuid.UUID:
        self.logger.info("Creating new budget")
        old_budget = self.close_budget(old_budget_id)
        old_date = datetime(old_budget.year, old_budget.month, 1)
        new_date = old_date + timedelta(days=31)
        budget_id = uuid.uuid4()
        budget = BudgetModel(
            id_=budget_id,
            month=new_date.month,
            year=new_date.year,
            is_current=True,
        )
        db.session.add(budget)
        db.session.commit()
        return budget_id

    @staticmethod
    def get_current_budget_id() -> uuid.UUID:
        return BudgetModel.query.filter_by(is_current=True).first().id_

    @staticmethod
    def get_budget_by_id(budget_id: uuid.UUID) -> BudgetModel:
        return BudgetModel.query.filter_by(id_=budget_id).first()

    @staticmethod
    def get_current_budget() -> BudgetModel:
        return BudgetModel.query.filter_by(is_current=True).first()
