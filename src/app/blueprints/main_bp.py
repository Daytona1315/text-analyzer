import json

from flask import (
    Blueprint,
    render_template,
    request,
    session,
    make_response,
    current_app,
)

from src.app.services.text import TextService
from src.app.services.file import FileService


main_bp = Blueprint(
    name='main',
    import_name=__name__,
)


@main_bp.route("/", methods=["GET"])
def root():
    session['init'] = True
    return render_template("index.html")


@main_bp.route("/analyze", methods=["POST"])
def analyze_text(text: str = None):
    redis = current_app.extensions['redis_service']
    user_id: str = session['user_id']
    if not text:
        text = request.form.get("text")
    result = TextService.analyze_text(text)
    redis.analysis_result_save(user_id, result)
    result_html = render_template(
        'partials/result.html',
        result=result
    )
    response = make_response(result_html)
    response.headers['HX-Trigger'] = 'historyNeedsUpdate'
    return response


@main_bp.route("/upload", methods=["POST"])
def upload_file():
    result: tuple = FileService.load_file(request)
    file_path, extension = result
    text: str = TextService.extract_text(
        file_path=file_path,
        extension=extension,
    )
    return analyze_text(text)


@main_bp.route("/history", methods=["GET"])
def get_history():
    redis = current_app.extensions['redis_service']
    user_id: str = session['user_id']
    history = redis.analysis_history_get(user_id)
    if len(history) == 0:
        history = None
    history_html = render_template(
        'partials/history.html',
        history=history
    )
    return history_html


@main_bp.route("/result-by-id/<analysis_id>", methods=["GET"])
def get_result_by_id(analysis_id: str):
    redis = current_app.extensions['redis_service']
    user_id: str = session['user_id']
    result: dict = redis.analysis_result_get(user_id, analysis_id)
    if result:
        return render_template(
            'partials/result.html',
            result=result
        )
    return render_template(
        'partials/error.html',
        message='Not found'
    )


@main_bp.route("/history", methods=["DELETE"])
def clear_history():
    redis = current_app.extensions['redis_service']
    user_id: str = session['user_id']
    redis.analysis_result_clear(user_id)
    response = make_response('')
    response.headers['HX-Trigger'] = 'historyNeedsUpdate'
    return response
