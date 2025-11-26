import uuid
from datetime import timedelta
from flask import (
    Flask,
    session,
)
from flask_session import Session

from src.celery.init import celery_init_app
from src.app.error_handlers import register_error_handlers
from src.app.services.nlp import NLPModels
from src.app.utils.config import Config
from src.db.redis.client import get_redis_connection


def create_app():
    app: Flask = Flask(__name__)
    app.secret_key = Config.secret_key
    app.config["MAX_CONTENT_LENGTH"] = Config.max_file_size
    app.config["UPLOAD_FOLDER"] = Config.upload_folder
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(
        minutes=Config.session_lifetime
    )
    register_error_handlers(app)

    # celery config
    app.config.from_mapping(
        CELERY=dict(
            broker_url=Config.celery_broker_url,
            result_backend=Config.celery_result_backend,
            task_ignore_result=True,
        )
    )
    celery_init_app(app)

    # preloading NLP models
    NLPModels.load_all()

    # redis
    app.config["SESSION_TYPE"] = "redis"
    app.config["SESSION_REDIS"] = get_redis_connection(
        db=Config.redis_db, decode_responses=False
    )
    Session(app)
    from src.app.services.redis import RedisService

    app.extensions["redis_service"] = RedisService()

    from src.app.blueprints.main_blueprint import main_blueprint
    from src.app.blueprints.history_blueprint import history_blueprint
    from src.app.blueprints.functions_bluprint import functions_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(history_blueprint)
    app.register_blueprint(functions_blueprint)

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
        if "user_id" not in session:
            session["user_id"] = str(uuid.uuid4())

    return app
