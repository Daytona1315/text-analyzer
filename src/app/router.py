from flask import (
    Blueprint,
    render_template,
    request,
)

from src.app.service import (
    TextService,
    load_file,
)
from src.app.utils.custom_exception import FileProcessingError


router = Blueprint('items', __name__)


@router.route("/", methods=["GET"])
def root():
    return render_template("index.html")


@router.route("/analyze", methods=["POST"])
def analyze_text():
    text = request.form.get("text")
    result = TextService.analyze_text(text)
    return render_template(
        "partials/result.html",
        result=result
    )


@router.route("/upload", methods=["POST"])
def upload_file():
    try:
        file_path, extension = load_file(request)
        text = TextService.extract_text(
            file_path=file_path,
            extension=extension,
        )
        result = TextService.analyze_text(text)
        return render_template(
            'partials/result.html',
            result=result)
    except FileProcessingError as e:
        return render_template(
            'partials/error.html',
            message=e.message
        )
