from flask import (
    Blueprint,
    render_template,
    request,
)

from src.app.service import file_upload
from src.app.service import count_text, file_upload


router = Blueprint('items', __name__)


@router.route("/", methods=["GET"])
def root():
    return render_template("index.html")


@router.route("/analyze", methods=["POST"])
def analyze_text():
    text = request.form.get("text")
    dictionary = count_text(text)
    return render_template(
        "partials/result.html",
        dictionary=dictionary
    )


@router.route("/upload", methods=["POST"])
def upload_file():
    if request.method == 'POST':
        result = file_upload()
