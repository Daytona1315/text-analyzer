import os

from src.app.utils.strtobool import strtobool


# Separate file to load all the dependencies

class Config:
    allowed_extensions: list = os.getenv('ALLOWED_EXTENSIONS').split(",")

    max_file_size: int = int(os.getenv('MAX_FILE_SIZE'))

    secret_key: str = os.getenv('SECRET_KEY', 'fallback-secret')

    file_cleanup_threshold: int = int(os.getenv('FILE_CLEANUP_THRESHOLD'))

    file_cleanup_sleep: int = int(os.getenv('FILE_CLEANUP_SLEEP'))

    is_session_permanent: bool = strtobool(os.getenv('IS_SESSION_PERMANENT'))  # validated by strtobool.py

    session_lifetime: int = int(os.getenv('SESSION_LIFETIME'))  # value in minutes (1 = one minute)

    upload_folder: str = os.getenv('UPLOAD_FOLDER')

    # redis
    redis_host: str = os.getenv('REDIS_HOST', 'localhost')

    redis_port: int = int(os.getenv('REDIS_PORT', 6379))

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.isabs(upload_folder):
        upload_folder = os.path.join(BASE_DIR, upload_folder)
