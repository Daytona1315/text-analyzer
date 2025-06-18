from flask import (
    Blueprint,
    render_template,
    request,
)

from src.app.service import (
    TextService,
    load_file,
)
from app.utils.custom_exception import FileProcessingError


router = Blueprint('items', __name__)


@router.route("/", methods=["GET"])
def root():
    return render_template("index.html")


@router.route("/analyze", methods=["POST"])
def analyze_text():
    text = request.form.get("text")
    dictionary = TextService.count_text(text)
    return render_template(
        "partials/result.html",
        dictionary=dictionary
    )


@router.route("/upload", methods=["POST"])
def upload_file():
    try:
        file_path, extension = load_file(request)
        text = TextService.extract_text(
            file_path=file_path,
            extension=extension,
        )
        dictionary = TextService.count_text(text)
        return render_template(
            'partials/result.html',
            dictionary=dictionary)
    except FileProcessingError as e:
        return render_template(
            'partials/error.html',
            message=e.message
        )
