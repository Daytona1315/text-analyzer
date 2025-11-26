import os
from dotenv import load_dotenv
from src.app.utils.strtobool import strtobool


load_dotenv()


class Config:

    base_dir: str = os.getenv("BASE_DIR", "src/app")

    _allowed_ext_raw = os.getenv("ALLOWED_EXTENSIONS", "txt,pdf,doc,docx")
    allowed_extensions: list = _allowed_ext_raw.split(",")

    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", 10485760))  # 10 MB

    secret_key: str = os.getenv("SECRET_KEY", "fallback-secret-key-change-me")

    is_session_permanent: bool = strtobool(os.getenv("IS_SESSION_PERMANENT", "False"))

    session_lifetime: int = int(os.getenv("SESSION_LIFETIME", 300))

    upload_folder: str = os.getenv("UPLOAD_FOLDER", "static/files")

    # NLP
    _nlp_langs_raw = os.getenv("NLP_LANGS", "ru,en")
    nlp_langs: list = _nlp_langs_raw.split(",")
    nlp_models_raw = os.getenv("NLP_MODELS", "en:en_core_web_sm,ru:ru_core_news_sm")
    try:
        nlp_models = dict(
            item.split(":") for item in nlp_models_raw.split(",") if ":" in item
        )
        if not nlp_models:
            raise ValueError
    except Exception:
        nlp_models = {"ru": "ru_core_news_sm", "en": "en_core_web_sm"}

    # Redis
    redis_host: str = os.getenv("REDIS_HOST", "127.0.0.1")
    redis_port: int = int(os.getenv("REDIS_PORT", 6379))
    redis_db: int = int(os.getenv("REDIS_DB", 0))
    redis_max_count: int = int(os.getenv("REDIS_MAX_COUNT", 30))
    redis_record_expire: int = int(os.getenv("REDIS_RECORD_EXPIRE", 18000))
    redis_service_db: int = int(os.getenv("REDIS_SERVICE_DB", 1))

    # Celery
    celery_db: int = int(os.getenv("CELERY_DB", 2))
    celery_broker_url: str = f"redis://{redis_host}:{redis_port}/{celery_db}"
    celery_result_backend: str = f"redis://{redis_host}:{redis_port}/{celery_db}"
