from celery import shared_task
from celery.utils.log import get_task_logger
from flask import current_app
from src.app.services.text import TextService


logger = get_task_logger(__name__)

@shared_task(ignore_result=False)
def analyze_text_task(text: str, user_id: str):
    try:
        logger.info(f"👷 [Worker] RECEIVED task for User: {user_id}")
        result = TextService.analyze_text(text)
        redis_service = current_app.extensions["redis_service"]
        redis_service.analysis_result_save(user_id, result)
        logger.info(f"🏁 [Worker] FINISHED task successfully")
        return result
    except Exception as e:
            logger.error(f"🔥 [Worker] FAILED task: {e}", exc_info=True) # <--- Лог ошибки
            raise e
