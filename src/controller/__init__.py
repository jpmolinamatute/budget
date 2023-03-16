import logging

from sqlalchemy.orm import Session

from src.controller.bill_controller import BillController, primitiveBill
from src.controller.budget_controller import BudgetController
from src.controller.income_controller import IncomeController
from src.controller.plan_controller import PlanController, primitivePlan


def create_new_budget(logger: logging.Logger, session: Session) -> None:
    budget = BudgetController(logger, session)
    old_budget = budget.close_budget()
    budget.create(old_budget)
    bill = BillController(logger, session, budget)
    bill.create()
    plan = PlanController(logger, session, budget)
    plan.create(old_budget.id_)
    income = IncomeController(logger, session, budget)
    income.create(old_budget.id_)


__all__ = [
    "BillController",
    "BudgetController",
    "IncomeController",
    "PlanController",
    "create_new_budget",
    "primitiveBill",
    "primitivePlan",
]
