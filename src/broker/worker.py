from src.app.main import create_app


app = create_app()
celery = app.extensions["broker"]
