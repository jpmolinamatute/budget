# import uuid

from http import HTTPStatus

from flask import Blueprint, Response, abort, current_app, request


# from src.controller.complete_budget_controler import CompleteBudgetControler


db_endpoint = Blueprint("db_endpoint", __name__)


@db_endpoint.route("/budget", methods=["POST"])
def create_budget():
    content = request.json
    current_app.logger.info(content)
    # old_budget = uuid.UUID(content["old_budget"])
    try:
        # budget = CompleteBudgetControler()
        # budget.new_budget(old_budget)
        # budget.process()
        pass
    except Exception as e:
        current_app.logger.error(e)
        abort(HTTPStatus.BAD_REQUEST, e)
    return Response("Budget created\n", HTTPStatus.CREATED)
