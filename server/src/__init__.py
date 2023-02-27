from os import environ

from flask import Flask

from src.model import db
from src.model.bill_model import BillModel
from src.model.bill_template_model import BillTemplateModel
from src.model.budget_model import BudgetModel
from src.model.enums import payment_type, provider_type
from src.model.income_model import IncomeModel
from src.model.payment_plan_model import PaymentPlanModel
from src.routes.db_route import db_endpoint
from src.routes.web_route import web_endpoint


def create_app():
    database = environ["POSTGRES_DATABASE"]
    user = environ["POSTGRES_USER"]
    password = environ["POSTGRES_PASSWORD"]
    host = environ["POSTGRES_HOST"]
    port = environ["POSTGRES_PORT"]
    app = Flask(__name__, instance_relative_config=True)
    database_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    app.config.from_mapping(
        SECRET_KEY="development",
        SQLALCHEMY_DATABASE_URI=database_uri,
    )

    app.register_blueprint(db_endpoint)
    app.register_blueprint(web_endpoint)
    db.init_app(app)

    return app


__all__ = [
    "BudgetModel",
    "BillModel",
    "IncomeModel",
    "PaymentPlanModel",
    "BillTemplateModel",
    "payment_type",
    "provider_type",
    "create_app",
]
