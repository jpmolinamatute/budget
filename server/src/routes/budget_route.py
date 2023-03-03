from http import HTTPStatus

from flask import Blueprint, Response, abort, current_app, request, jsonify
from src.controller import create_new_budget, BudgetController, PlanController


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
