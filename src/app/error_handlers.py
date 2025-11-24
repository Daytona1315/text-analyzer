from flask import render_template
from werkzeug.exceptions import HTTPException

from src.app.utils.logging import log
from src.app.utils.custom_exceptions import BaseAppException


def register_error_handlers(app):
    @app.errorhandler(BaseAppException)
    def handle_custom_exception(e: BaseAppException):
        return render_template("partials/error.html", message=e.message)

    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        return render_template("partials/error.html", message=e.description)

    @app.errorhandler(Exception)
    def handle_unexpected_exception(e: Exception):
        log.exception("Unexpected error occurred: %s", e)
        return render_template(
            "partials/error.html", message="Something went wrong. Please, try later."
        )

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html")
