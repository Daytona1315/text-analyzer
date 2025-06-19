import os
import time

from flask import current_app

from src.app.utils.env_loader import Config


def cleanup_old_files() -> None:
    """
    Deletes old files except __init__.py.
    """
    while True:
        folder: str = current_app.config['UPLOAD_FOLDER']
        threshold: int = Config.file_cleanup_threshold
        now: float = time.time()
        for filename in os.listdir(folder):
            if filename == '__init__.py':
                continue  # не удалять
            path = os.path.join(folder, filename)
            if os.path.isfile(path):
                last_modified = os.path.getmtime(path)
                if now - last_modified > threshold:
                    os.remove(path)
                    print(f"Removed old file: {path}")
        time.sleep(Config.file_cleanup_sleep)
