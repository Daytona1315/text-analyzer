import os

from flask import (
    Blueprint, render_template,
    request, redirect,
    current_app, url_for,
)
from werkzeug.utils import secure_filename

from src.app.service import count_text, allowed_file

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
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file')
            return redirect(location="/")
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return redirect(location="/")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('router.download_file', name=filename))
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''