import uuid
import logging

from src.controller.budget_controller import BudgetController
from src.controller.bill_controller import BillController
from src.controller.income_controller import IncomeController
from src.controller.plan_controller import PlanController


def create_new_budget(old_budget_id: uuid.UUID) -> None:
    logger = logging.getLogger(__name__)
    budget = BudgetController(logger)
    budget.create(old_budget_id)
    plan = PlanController(logger)
    plan.create(old_budget_id)
    bill = BillController(logger)
    bill.create()
    income = IncomeController(logger)
    income.create(old_budget_id)
