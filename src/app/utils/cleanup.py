import os
import time

from flask import current_app

from src.app.utils.env_loader import Config


def cleanup_old_files() -> None:
    """
    Simply deletes files when they are getting old enough.
    Function 'sleeps' for the specified time and is called.
    """
    while True:
        folder: str = current_app.config['UPLOAD_FOLDER']
        threshold: int = Config.file_cleanup_threshold  # specified in .env (1 = one second)
        now: float = time.time()
        for filename in os.listdir(folder):
            path = os.path.join(folder, filename)
            if os.path.isfile(path):
                last_modified = os.path.getmtime(path)
                if now - last_modified > threshold:
                    os.remove(path)
                    print(f"Removed old file: {path}")
        time.sleep(Config.file_cleanup_sleep)  # specified in .env (1 = 1 second)
