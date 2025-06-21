import os

from dotenv import load_dotenv

from src.app.utils.strtobool import strtobool


load_dotenv()


class Config:
    allowed_extensions: list = os.getenv('ALLOWED_EXTENSIONS').split(",")

    max_file_size: int = int(os.getenv('MAX_FILE_SIZE'))

    secret_key: str = os.getenv('SECRET_KEY', 'fallback-secret')

    is_session_permanent: bool = strtobool(os.getenv('IS_SESSION_PERMANENT'))

    session_lifetime: int = int(os.getenv('SESSION_LIFETIME'))  # value in minutes (1 = one minute)

    upload_folder: str = os.getenv('UPLOAD_FOLDER')

    # redis
    redis_host: str = os.getenv('REDIS_HOST', 'redis')

    redis_port: int = int(os.getenv('REDIS_PORT', 6379))

    redis_max_count: int = int(os.getenv('REDIS_MAX_COUNT'))  # maximal number of saved analysis results

    redis_record_expire: int = int(os.getenv('REDIS_RECORD_EXPIRE'))  # lifetime of record

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.isabs(upload_folder):
        upload_folder = os.path.join(BASE_DIR, upload_folder)
