import os

from dotenv import load_dotenv

from src.app.utils.strtobool import strtobool


load_dotenv()


class Config:
    base_dir: str = os.getenv("BASE_DIR")
    allowed_extensions: list = os.getenv("ALLOWED_EXTENSIONS").split(",")
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE"))
    secret_key: str = os.getenv("SECRET_KEY", "fallback-secret")
    is_session_permanent: bool = strtobool(os.getenv("IS_SESSION_PERMANENT"))
    session_lifetime: int = int(
        os.getenv("SESSION_LIFETIME")
    )  # value in minutes (1 = one minute)
    upload_folder: str = os.getenv("UPLOAD_FOLDER")

    # nlp
    nlp_langs: list = os.getenv("NLP_LANGS").split(",")
    nlp_models_raw = os.getenv("NLP_MODELS", "")
    try:
        nlp_models = dict(
            item.split(":") for item in nlp_models_raw.split(",") if ":" in item
        )
        if not nlp_models:
            raise ValueError
    except Exception:
        # fallback to default
        nlp_models = {"ru": "ru_core_news_sm", "en": "en_core_web_sm"}

    # redis
    redis_host: str = os.getenv("REDIS_HOST", "redis")
    redis_port: int = int(os.getenv("REDIS_PORT", 6379))
    redis_db: int = int(os.getenv("REDIS_DB", 0))
    redis_max_count: int = int(
        os.getenv("REDIS_MAX_COUNT")
    )  # maximal number of saved analysis results
    redis_record_expire: int = int(
        os.getenv("REDIS_RECORD_EXPIRE")
    )  # lifetime of record

    # celery
    celery_db: int = int(os.getenv("CELERY_DB", 0))
    celery_broker_url: str = f"redis://{redis_host}:{redis_port}/{celery_db}"
    celery_result_backend: str = f"redis://{redis_host}:{redis_port}/{celery_db}"
