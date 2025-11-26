import os
import sys

from src.app.main import create_app
from src.app.utils.config import Config

# --- DEBUG START ---
# Выводим настройки прямо в stdout перед запуском
print("--- WORKER STARTUP DEBUG ---")
print(f"DEBUG: REDIS_HOST = {os.getenv('REDIS_HOST')}")
print(f"DEBUG: CELERY_DB = {os.getenv('CELERY_DB')}")
print(f"DEBUG: Broker URL = {Config.celery_broker_url}")
print("----------------------------")
sys.stdout.flush()
# --- DEBUG END ---

app = create_app()
celery = app.extensions["broker"]
