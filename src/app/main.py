from flask import Flask

from src.app.router import router


app = Flask(__name__)
app.register_blueprint(router)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = '/app/files'

if __name__ == "__main__":
    app.run(debug=True)
