import uuid
import threading
from datetime import timedelta
from flask import (
    Flask,
    session,
    render_template,
)
from flask_session import Session
from werkzeug.exceptions import RequestEntityTooLarge

from src.app.utils.cleanup import cleanup_old_files
from src.app.utils.env_loader import Config
from src.db.redis import get_redis_connection


def create_app():
    app = Flask(__name__)
    app.secret_key = Config.secret_key
    app.config['MAX_CONTENT_LENGTH'] = Config.max_file_size
    app.config['UPLOAD_FOLDER'] = Config.upload_folder
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=Config.session_lifetime)

    # Redis connection block

    # redis for sessions
    # as Flask-Session expect to work with bytes,
    # decode_responses parameter set to False
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = get_redis_connection(db=0, decode_responses=False)
    Session(app)

    # redis for history
    # as we work here with strings,
    # decode_responses parameter set to True
    app.redis_history = get_redis_connection(db=1, decode_responses=True)

    from app.blueprints.main_bp import main_bp
    app.register_blueprint(main_bp)

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
        session.permanent = Config.is_session_permanent
        return None

    @app.before_request
    def set_user_id() -> None:
        """
        Initializes session. Creates uuid for user.
        It is placed in session, other private values
        may be added there also.
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
