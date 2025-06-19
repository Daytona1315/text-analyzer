from flask import (
    Blueprint,
    render_template,
    request,
    session,
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
    user_id = session['user_id']
    if not text:
        text = request.form.get("text")
    result = TextService.analyze_text(text)
    HistoryService.save_history(user_id, data=result['preview'])
    history = HistoryService.get_history(user_id)
    return render_template(
        "partials/result_with_history.html",
        result=result,
        history=history,
    )


@main_bp.route("/upload", methods=["POST"])
def upload_file():
    try:
        file_path, extension = FileService.load_file(request)
        text = TextService.extract_text(
            file_path=file_path,
            extension=extension,
        )
        return analyze_text(text)
    except FileProcessingError as e:
        return render_template(
            'partials/error.html',
            message=e.message
        )
