from flask import (
    Blueprint,
    current_app,
    session,
    make_response,
    render_template,
)

history_bp = Blueprint(
    name='history',
    import_name=__name__,
)


@history_bp.route("/history", methods=["GET"])
def get_history():
    redis = current_app.extensions['redis_service']
    user_id: str = session['user_id']
    history = redis.analysis_history_get(user_id)
    if len(history) == 0:
        history = None
    history_html = render_template(
        'partials/history.html',
        history=history
    )
    return history_html


@history_bp.route("/history", methods=["DELETE"])
def clear_history():
    redis = current_app.extensions['redis_service']
    user_id: str = session['user_id']
    redis.analysis_result_clear(user_id)
    response = make_response('')
    response.headers['HX-Trigger'] = 'historyNeedsUpdate'
    return response
