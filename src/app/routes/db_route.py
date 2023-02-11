from flask import Blueprint


db_endpoint = Blueprint("db_endpoint", __name__)


@db_endpoint.route("/budget", methods=["GET", "POST", "UPDATE", "DELETE"])
def budget():
    """base index view"""
    return "<p>Hello, World!</p>"
