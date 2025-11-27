from functools import wraps
from flask import (
    current_app,
    session,
)

from src.app.consts import SessionKeys
from src.app.services.functions import FunctionsService
from src.app.services.redis import RedisService


def inject_functions_service(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        redis = current_app.extensions["redis_service"]
        user_id: str = session[SessionKeys.USER_ID]
        analysis_id: str = session[SessionKeys.ACTIVE_ANALYSIS_ID]
        analysis_result: dict = redis.analysis_result_get(user_id, analysis_id)

        kwargs["functions_service"] = FunctionsService(
            redis=redis,
            user_id=user_id,
            analysis_result=analysis_result,
        )
        return func(*args, **kwargs)

    return wrapper
