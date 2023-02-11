from flask import Blueprint


web_endpoint = Blueprint("web_endpoint", __name__)


@web_endpoint.route("/")
@web_endpoint.route("/index")
def index():
    """base index view"""
    return "<p>Hello, World!</p>"
