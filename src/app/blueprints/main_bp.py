from flask import (
    Blueprint,
    render_template,
    request,
    session, render_template_string, make_response,
)

from src.app.services.history import HistoryService
from src.app.services.text import TextService
from src.app.services.file import FileService
from src.app.utils.custom_exception import FileProcessingError


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
    user_id: str = session['user_id']
    if not text:
        text = request.form.get("text")
    result = TextService.analyze_text(text)
    HistoryService.history_save(user_id, data=result['preview'])

    result_html = render_template(
        'partials/result.html',
        result=result
    )

    response = make_response(result_html)
    response.headers['HX-Trigger'] = 'historyNeedsUpdate'
    return response


@main_bp.route("/upload", methods=["POST"])
def upload_file():
    try:
        file_path, extension = FileService.load_file(request)
        text = TextService.extract_text(
            file_path=file_path,
            extension=extension,
        )
        return analyze_text(text=text)
    except FileProcessingError as e:
        return render_template(
            'partials/error.html',
            message=e.message
        )


@main_bp.route("/history", methods=["GET"])
def get_history():
    user_id: str = session['user_id']
    history = HistoryService.history_get(user_id)
    if len(history) == 0:
        history = ""
    history_html = render_template(
        'partials/history.html',
        history=history
    )
    return history_html


@main_bp.route("/history", methods=["DELETE"])
def clear_history():
    user_id: str = session['user_id']
    HistoryService.history_clear(user_id)
    response = make_response('')
    response.headers['HX-Trigger'] = 'historyNeedsUpdate'
    return response
