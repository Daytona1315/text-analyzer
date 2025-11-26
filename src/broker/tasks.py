from celery import shared_task
from flask import current_app
from src.app.services.text import TextService


@shared_task(ignore_result=False)
def analyze_text_task(text: str, user_id: str):
    result = TextService.analyze_text(text)
    redis_service = current_app.extensions["redis_service"]
    redis_service.analysis_result_save(user_id, result)
    return result
