from os import environ

from flask import Flask

from src.app.models import db
from src.app.models.enums import payment_type, provider_type
from src.app.routes.basic import endpoint


from src.app.models.budget import Budget  # isort:skip
from src.app.models.bill import Bill  # isort:skip
from src.app.models.salary import Salary  # isort:skip
from src.app.models.payment_plan import PaymentPlan  # isort:skip


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

    app.register_blueprint(endpoint)
    db.init_app(app)

    return app


__all__ = ["Budget", "Bill", "Salary", "PaymentPlan", "payment_type", "provider_type", "create_app"]
