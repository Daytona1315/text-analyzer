import os
from flask import Flask
from dotenv import load_dotenv

from src.app.router import router

load_dotenv()
upload_folder = os.getenv('UPLOAD_FOLDER')
if not os.path.isabs(upload_folder):
    upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), upload_folder)

app = Flask(__name__)
app.register_blueprint(router)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = upload_folder

if __name__ == "__main__":
    app.run(debug=True)
