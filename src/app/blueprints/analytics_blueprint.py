from flask import (
    Blueprint,
    render_template,
)

from src.app.services.analytics import AnalyticsService
from src.app.utils.custom_exceptions import BaseAppException
from src.app.services.file import FileService


analytics_blueprint = Blueprint(
    name="functions",
    import_name=__name__,
)


@analytics_blueprint.route("/word-cloud", methods=["GET"])
def word_cloud():
    try:
        service = AnalyticsService.create_from_session()
        svg: str = service.generate_word_cloud()
        return render_template(
            "partials/word-cloud.html",
            svg=svg,
        )
    except BaseAppException as e:
        return render_template("partials/error.html", message=e.message)


@analytics_blueprint.route("/lemmatization", methods=["GET"])
def lemmatization():
    try:
        service = AnalyticsService.create_from_session()
        result: list = service.generate_lemmatization()
        path = FileService.write_csv(result)
    except BaseAppException as e:
        return render_template("partials/error.html", message=e.message)
    return render_template(
        "partials/lemmatization.html",
        path=path,
    )

@analytics_blueprint.route("/ner", methods=["GET"])
def ner():
    try:
        service = AnalyticsService.create_from_session()
        html: str = service.generate_ner()
        return render_template("partials/ner.html", html=html)
    except BaseAppException as e:
        return render_template("partials/error.html", message=e.message)
