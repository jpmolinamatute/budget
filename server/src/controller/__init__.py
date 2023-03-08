import logging

from src.controller.bill_controller import BillController, primitiveBill
from src.controller.budget_controller import BudgetController, SimpleBudget
from src.controller.income_controller import IncomeController
from src.controller.plan_controller import PlanController, primitivePlan


def create_new_budget(logger: logging.Logger) -> None:
    budget = BudgetController(logger)
    old_budget_id = budget.get_current_budget_id()
    budget.create(old_budget_id)
    bill = BillController(logger)
    bill.create()
    plan = PlanController(logger)
    plan.create(old_budget_id)
    income = IncomeController(logger)
    income.create(old_budget_id)


__all__ = [
    "BillController",
    "BudgetController",
    "IncomeController",
    "PlanController",
    "create_new_budget",
    "primitiveBill",
    "SimpleBudget",
    "primitivePlan",
]
