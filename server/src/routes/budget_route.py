import uuid
from datetime import datetime
from http import HTTPStatus

from flask import Blueprint, Response, abort, current_app, jsonify, request

from src.controller import BudgetController, PlanController, IncomeController, create_new_budget


budget_route = Blueprint("budget_route", __name__, url_prefix="/api/v1")


@budget_route.route("/budget", methods=["POST"])
def create_budget():
    content = request.json
    current_app.logger.info(content)
    try:
        create_new_budget(current_app.logger)
    except Exception as e:
        current_app.logger.error(e)
        abort(HTTPStatus.BAD_REQUEST, e)
    return Response("Budget created\n", HTTPStatus.CREATED)


@budget_route.route("/budget", methods=["GET"])
def get_budget():
    budget = BudgetController.get_current_budget()
    return jsonify(budget)


@budget_route.route("/plan", methods=["GET"])
def get_plan():
    plan = PlanController.get_current_plan()
    return jsonify(plan)


@budget_route.route("/plan", methods=["UPDATE"])
def update_plan():
    content = request.json
    plan_item_id = uuid.UUID(content["plan_item_id"])
    PlanController.update__plan_item_amount(plan_item_id, content["amount"])
    return Response("Plan updated\n", HTTPStatus.OK)


@budget_route.route("/plan/close", methods=["UPDATE"])
def close_plan():
    content = request.json
    plan_item_id = uuid.UUID(content["plan_item_id"])
    PlanController.mark_plan_item_closed(plan_item_id)
    return Response("Plan updated\n", HTTPStatus.OK)


@budget_route.route("/plan/reopen", methods=["UPDATE"])
def reopen_plan():
    content = request.json
    plan_item_id = uuid.UUID(content["plan_item_id"])
    PlanController.mark_plan_item_opened(plan_item_id)
    return Response("Plan updated\n", HTTPStatus.OK)


@budget_route.route("/income", methods=["GET"])
def get_income():
    income = IncomeController.get_incomes()
    return jsonify(income)


@budget_route.route("/income", methods=["POST"])
def add_income():
    content = request.json
    date_obj = datetime.strptime(content["date"], "%Y-%m-%d")
    IncomeController.add_other_income(content["amount"], date_obj)
    return Response("Income added\n", HTTPStatus.CREATED)


@budget_route.route("/income", methods=["UPDATE"])
def update_income():
    content = request.json
    content["income_id"] = uuid.UUID(content["income_id"])
    IncomeController.update_income(**content)
    return Response("Income updated\n", HTTPStatus.OK)
