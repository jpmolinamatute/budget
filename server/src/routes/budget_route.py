import uuid

from datetime import datetime
from http import HTTPStatus
from typing import Any, Optional

from flask import Blueprint, abort, current_app, request

from src.controller import (
    BillController,
    BudgetController,
    IncomeController,
    PlanController,
    SimpleBudget,
    create_new_budget,
    primitiveBill,
    primitivePlan,
)

# @TODO: write tests for all routes
# @TODO: improve validation of request.json
# @TODO: improve error handling

budget_route = Blueprint("budget_route", __name__, url_prefix="/api/v1")


def return_uuid(content: Optional[Any], key: str) -> uuid.UUID:
    if content is None:
        raise ValueError("Request json is empty")
    if key not in content:
        raise ValueError(f"Request json does not contain key {key}")
    return uuid.UUID(content[key], version=4)


def return_datetime(content: Optional[Any], key: str) -> datetime:
    if content is None:
        raise ValueError("Request json is empty")
    if key not in content:
        raise ValueError(f"Request json does not contain key {key}")
    return datetime.fromisoformat(content[key])


@budget_route.route("/budget", methods=["POST"])
def create_budget() -> tuple[str, int]:
    content = request.json
    try:
        if content is None:
            raise ValueError("Request json is empty")
        create_new_budget(current_app.logger)
    except Exception as e:
        current_app.logger.error(e)
        abort(HTTPStatus.BAD_REQUEST, e)
    return "Budget created\n", HTTPStatus.CREATED


@budget_route.route("/budget", methods=["GET"])
def get_budget() -> tuple[SimpleBudget, int]:
    try:
        budget = BudgetController.get_current_budget()
    except Exception as e:
        current_app.logger.error(e)
        abort(HTTPStatus.BAD_REQUEST, e)
    return budget, HTTPStatus.OK


@budget_route.route("/plan", methods=["GET"])
def get_plan() -> tuple[list[primitivePlan], int]:
    try:
        plan = PlanController.get_current_plan()
    except Exception as e:
        current_app.logger.error(e)
        abort(HTTPStatus.BAD_REQUEST, e)
    return plan, HTTPStatus.OK


@budget_route.route("/plan", methods=["UPDATE"])
def update_plan() -> tuple[str, int]:
    content = request.json
    try:
        if content is None:
            raise ValueError("Request json is empty")
        plan_item_id = return_uuid(content, "plan_item_id")
        PlanController.update_plan_item_amount(plan_item_id, content["amount"])
    except Exception as e:
        current_app.logger.error(e)
        abort(HTTPStatus.BAD_REQUEST, e)
    return "Plan updated\n", HTTPStatus.OK


@budget_route.route("/plan/close", methods=["UPDATE"])
def close_plan() -> tuple[str, int]:
    content = request.json
    try:
        plan_item_id = return_uuid(content, "plan_item_id")
        PlanController.mark_plan_item_closed(plan_item_id)
    except Exception as e:
        current_app.logger.error(e)
        abort(HTTPStatus.BAD_REQUEST, e)
    return "Plan updated\n", HTTPStatus.OK


@budget_route.route("/plan/reopen", methods=["UPDATE"])
def reopen_plan() -> tuple[str, int]:
    content = request.json
    try:
        plan_item_id = return_uuid(content, "plan_item_id")
        PlanController.mark_plan_item_opened(plan_item_id)
    except Exception as e:
        current_app.logger.error(e)
        abort(HTTPStatus.BAD_REQUEST, e)
    return "Plan updated\n", HTTPStatus.OK


@budget_route.route("/income", methods=["GET"])
def get_income() -> tuple[list, int]:
    try:
        income = IncomeController.get_current_income()
    except Exception as e:
        current_app.logger.error(e)
        abort(HTTPStatus.BAD_REQUEST, e)
    return income, HTTPStatus.OK


@budget_route.route("/income", methods=["POST"])
def add_income():
    content = request.json
    try:
        if content is None:
            raise ValueError("Request json is empty")
        date_obj = return_datetime(content, "date")
        IncomeController.add_income(content["amount"], date_obj, content["income_type"])
    except Exception as e:
        current_app.logger.error(e)
        abort(HTTPStatus.BAD_REQUEST, e)
    return "Income added\n", HTTPStatus.CREATED


@budget_route.route("/income", methods=["UPDATE"])
def update_income() -> tuple[str, int]:
    content = request.json
    try:
        if content is None:
            raise ValueError("Request json is empty")
        income_id = return_uuid(content, "income_id")
        if "amount" in content and isinstance(content["amount"], (int, float)):
            IncomeController.update_income_amount(income_id, content["amount"])
        if "date" in content:
            date_obj = return_datetime(content, "date")
            IncomeController.update_income_date(income_id, date_obj)
        if "income_type" in content:
            IncomeController.update_income_type(income_id, content["income_type"])
    except Exception as e:
        current_app.logger.error(e)
        abort(HTTPStatus.BAD_REQUEST, e)
    return "Income updated\n", HTTPStatus.OK


@budget_route.route("/income", methods=["DELETE"])
def delete_income() -> tuple[str, int]:
    content = request.json
    try:
        if content is None:
            raise ValueError("Request json is empty")
        income_id = return_uuid(content, "income_id")
        IncomeController.delete_income(income_id)
    except Exception as e:
        current_app.logger.error(e)
        abort(HTTPStatus.BAD_REQUEST, e)
    return "Income deleted\n", HTTPStatus.OK


@budget_route.route("/bill", methods=["GET"])
def get_bill() -> tuple[list[primitiveBill], int]:
    try:
        bills = BillController.get_current_bill()
    except Exception as e:
        current_app.logger.error(e)
        abort(HTTPStatus.BAD_REQUEST, e)
    return bills, HTTPStatus.OK


@budget_route.route("/bill", methods=["UPDATE"])
def update_bill() -> tuple[str, int]:
    content = request.json
    try:
        if content is None:
            raise ValueError("Request json is empty")
        bill_id = return_uuid(content, "bill_id")
        if "amount" in content and isinstance(content["amount"], (int, float)):
            BillController.update_bill_amount(bill_id, content["amount"])
        if "due_date" in content and isinstance(content["due_date"], str):
            due_date = return_datetime(content, "due_date")
            BillController.update_bill_due_date(bill_id, due_date)
    except Exception as e:
        current_app.logger.error(e)
        abort(HTTPStatus.BAD_REQUEST, e)
    return "Bill updated\n", HTTPStatus.OK


@budget_route.route("/bill/close", methods=["UPDATE"])
def close_bill() -> tuple[str, int]:
    content = request.json
    try:
        bill_id = return_uuid(content, "bill_id")
        BillController.mark_bill_paid(bill_id)
    except Exception as e:
        current_app.logger.error(e)
        abort(HTTPStatus.BAD_REQUEST, e)
    return "Bill closed\n", HTTPStatus.OK


@budget_route.route("/bill/reopen", methods=["UPDATE"])
def reopen_bill() -> tuple[str, int]:
    content = request.json
    try:
        bill_id = return_uuid(content, "bill_id")
        BillController.mark_bill_unpaid(bill_id)
    except Exception as e:
        current_app.logger.error(e)
        abort(HTTPStatus.BAD_REQUEST, e)
    return "Bill reopened\n", HTTPStatus.OK
