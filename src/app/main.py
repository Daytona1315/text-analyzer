import uuid
from datetime import timedelta
from flask import (
    Flask,
    session,
    render_template, make_response, Response,
)
from flask_session import Session
from werkzeug.exceptions import RequestEntityTooLarge

from app.services.functions import NLPModels
from app.utils.custom_exceptions import FileIsEmpty
from src.app.utils.config import Config
from src.db.redis_client import get_redis_connection
from src.app.utils.custom_exceptions import UnsupportedFileType


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

    # preloading NLP models
    NLPModels.load_all()

    # redis for business logic
    from src.app.services.redis import RedisService
    app.extensions['redis_service'] = RedisService()

    from src.app.blueprints.main_bp import main_bp
    from src.app.blueprints.history_bp import history_bp
    from src.app.blueprints.functions_bp import functions_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(functions_bp)

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
            session['user_id'] = str(uuid.uuid4())

    # 'error handler' section
    @app.errorhandler(RequestEntityTooLarge)
    def file_too_large(e) -> Response:
        response = make_response(
            render_template(
                'partials/error.html',
                message='File is too large'
            )
        )
        response.headers['HX-Target'] = '#error'
        return response

    @app.errorhandler(UnsupportedFileType)
    def file_unsupported(e) -> Response:
        response = make_response(
            render_template(
                'partials/error.html',
                message='File is not allowed'
            )
        )
        response.headers['HX-Target'] = '#error'
        return response

    @app.errorhandler(FileIsEmpty)
    def file_is_empty(e) -> Response:
        response = make_response(
            render_template(
                'partials/error.html',
                message='File is empty'
            )
        )
        response.headers['HX-Target'] = '#error'
        return response

    @app.errorhandler(404)
    def page_not_found(e) -> str:
        return render_template(
            '404.html'
        )

    return app
