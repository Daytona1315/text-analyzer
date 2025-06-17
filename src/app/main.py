import os
import uuid

from flask import (
    Flask,
    session,
)
from dotenv import load_dotenv


load_dotenv()
allowed_extensions: list = os.getenv('ALLOWED_EXTENSIONS').split(",")
secret_key: str = os.getenv('SECRET_KEY')
upload_folder: str = os.getenv('UPLOAD_FOLDER')
if not os.path.isabs(upload_folder):
    upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), upload_folder)


def create_app():
    app = Flask(__name__)
    app.secret_key = secret_key
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = upload_folder

    from src.app.router import router
    app.register_blueprint(router)

    @app.before_request
    def set_user_id() -> None:
        """
        Creates uuid for every user. It is placed in list,
        other private values may be added there also.
        """
        if 'user_id' not in session:
            session['user_id'] = [str(uuid.uuid4())]
            print(session)
    return app
