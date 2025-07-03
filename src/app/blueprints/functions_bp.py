from flask import (
    Blueprint,
    render_template,
)

from src.app.utils.custom_exceptions import BaseAppException
from src.app.services.file import FileService
from src.app.utils.decorators import inject_functions_service

functions_bp = Blueprint(
    name='functions',
    import_name=__name__,
)


@functions_bp.route('/word-cloud', methods=['GET'])
@inject_functions_service
def word_cloud(functions_service):
    try:
        svg: str = functions_service.generate_word_cloud()
        return render_template(
            'partials/word-cloud.html',
            svg=svg,
        )
    except BaseAppException as e:
        return render_template(
            'partials/error.html',
            message=e.message
        )


@functions_bp.route('/lemmatization', methods=['GET'])
@inject_functions_service
def lemmatization(functions_service):
    try:
        result: list = functions_service.generate_lemmatization()
        path = FileService.write_csv(result)
    except BaseAppException as e:
        return render_template(
            'partials/error.html',
            message=e.message
        )
    return render_template(
        'partials/lemmatization.html',
        path=path,
    )
