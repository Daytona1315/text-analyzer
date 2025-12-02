from celery.result import AsyncResult
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    current_app,
    make_response,
)

from src.app.services.document import DocumentService
from src.app.utils.custom_exceptions import (
    FileException,
    RedisException,
)
from src.app.services.text import TextService
from src.app.services.file import FileService
from src.app.utils.logging import log
from src.app.consts import SessionKeys, HtmxEvents, TaskStatus

main_blueprint = Blueprint(
    name="main",
    import_name=__name__,
)


@main_blueprint.route("/", methods=["GET"])
def root():
    session[SessionKeys.INIT] = True
    return render_template("index.html")


@main_blueprint.route("/analyze", methods=["POST"])
def analyze_text():
    text = request.form.get("text")
    return TextService.provide_text_analysis(text)


@main_blueprint.route("/upload", methods=["POST"])
def upload_file():
    file_path, extension = FileService.load_file(request)
    text = DocumentService.read_content(
        file_path=file_path,
        extension=extension
    )
    if not text or not text.strip():
        raise FileException()
    return TextService.provide_text_analysis(text)


@main_blueprint.route("/status/<task_id>", methods=["GET"])
def task_status(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.state == TaskStatus.SUCCESS:
        result = task_result.result
        session[SessionKeys.ACTIVE_ANALYSIS_ID] = result["id"]
        result_html = render_template("partials/result.html", result=result)
        response = make_response(result_html)
        response.headers["HX-Trigger"] = HtmxEvents.HISTORY_UPDATE
        response.headers["HX-Scroll"] = "#result:top"
        return response
    elif task_result.state == TaskStatus.FAILURE:
        error_msg = str(task_result.result)
        log.error(error_msg)
        return render_template(
            "partials/error.html", message=f"Task failed, please, try again"
        )
    else:
        return render_template("partials/processing.html", task_id=task_id)


@main_blueprint.route("/result-by-id/<analysis_id>", methods=["GET"])
def get_result_by_id(analysis_id: str):
    redis = current_app.extensions["redis_service"]
    user_id: str = session[SessionKeys.USER_ID]
    result: dict = redis.analysis_result_get(user_id, analysis_id)
    session[SessionKeys.ACTIVE_ANALYSIS_ID] = analysis_id
    if result:
        return render_template("partials/result.html", result=result)
    raise RedisException()
