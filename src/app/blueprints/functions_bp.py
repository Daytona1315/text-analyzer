from flask import (
    Blueprint,
    current_app,
    session,
    make_response,
    render_template,
)

from app.services.functions import FunctionsService


functions_bp = Blueprint(
    name='functions',
    import_name=__name__,
)


@functions_bp.route('/word-cloud')
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
