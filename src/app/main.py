import uuid
import threading
from datetime import timedelta
from flask import (
    Flask,
    session,
    render_template,
)
from werkzeug.exceptions import RequestEntityTooLarge

from src.app.utils.cleanup import cleanup_old_files
from src.app.utils.env_loader import (
    secret_key,
    upload_folder,
    session_lifetime,
    max_file_size,
    is_session_permanent,
)


def create_app():
    app = Flask(__name__)
    app.secret_key = secret_key
    app.config['MAX_CONTENT_LENGTH'] = max_file_size
    app.config['UPLOAD_FOLDER'] = upload_folder
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=session_lifetime)

    from src.app.router import router
    app.register_blueprint(router)

    # starting cleanup in a separate thread
    def run_cleanup():
        with app.app_context():
            cleanup_old_files()

    threading.Thread(target=run_cleanup, daemon=True).start()

    # 'before request' section
    @app.before_request
    def make_session_permanent() -> None:
        """
        It is specified in .env whether the session will be
        permanent or not. By default, it is not, so after
        closing the browser the session will be closed as well.
        """
        session.permanent = is_session_permanent
        print(type(is_session_permanent))
        print(is_session_permanent)
        return None

    @app.before_request
    def set_user_id() -> None:
        """
        Creates uuid for user. It is placed in session,
        other private values may be added there also.
        """
        if 'user_id' not in session:
            session['user_id'] = [str(uuid.uuid4())]

    # 'error handler' section
    @app.errorhandler(RequestEntityTooLarge)
    def file_too_large(e) -> str:
        return render_template(
            'partials/error.html',
            message="File is too large."
        )

    @app.errorhandler(404)
    def page_not_found(e) -> str:
        return render_template(
            '404.html'
        )

    return app
