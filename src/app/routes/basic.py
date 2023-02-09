from flask import Blueprint


endpoint = Blueprint("endpoint", __name__)


@endpoint.route("/")
@endpoint.route("/index")
def index():
    """base index view"""
    return "<p>Hello, World!</p>"
