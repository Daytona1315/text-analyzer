import os
from flask import (
    Blueprint, render_template,
    request, redirect,
    current_app,
)
from werkzeug.utils import secure_filename

from src.app.service import (
    count_text,
    allowed_file,
    extract_text,
)

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


@router.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file')
            return redirect(location="/")
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return redirect(location="/")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            extension = os.path.splitext(filename)[1].lower()
            text = extract_text(file_path, extension)
            if not text:
                return 'Unsupported file type or empty file', 400

            dictionary = count_text(text)
            return render_template('partials/result.html', dictionary=dictionary)
    return render_template("index.html"), 200
