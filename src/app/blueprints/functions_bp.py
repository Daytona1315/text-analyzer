import os
from flask import (
    Blueprint,
    render_template,
    session,
)

from app.services.file import FileService
from app.services.functions import FunctionsService
from app.utils.env_loader import Config

functions_bp = Blueprint(
    name='functions',
    import_name=__name__,
)


@functions_bp.route('/word-cloud', methods=['GET'])
def word_cloud():
    svg_str: str = FunctionsService.generate_word_cloud()
    if not svg_str:
        return render_template(
            'partials/error.html',
            message='Not enough words to illustrate'
        )
    return render_template(
        'partials/word-cloud.html',
        svg_str=svg_str,
    )


@functions_bp.route('/lemmatization', methods=['GET'])
def lemmatization():
    result: list = FunctionsService.generate_lemmatization()
    if not result:
        return render_template(
            'partials/error.html',
            message='The language of the text is undefined. Try longer text.'
        )
    path = FileService.write_csv(result)
    return render_template(
        'partials/lemmatization.html',
        path=path,
    )
