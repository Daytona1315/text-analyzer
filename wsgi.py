from src.app.utils.logging import log
from src.app.main import create_app


app = create_app()
if app:
    log.info("App created")
else:
    log.critical("APP IS NOT CREATED")
