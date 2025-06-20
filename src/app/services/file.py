import os

from flask import (
    Request,
    session,
    current_app,
)
from werkzeug.utils import secure_filename

from src.app.utils.custom_exception import FileProcessingError
from src.app.utils.env_loader import Config


class FileService:
    """
    Contains necessary methods related to files.
    """

    @classmethod
    def touch(cls, path: str) -> None:
        """
        Refresh file's 'mtime' to current time to prevent cleanup.
        It is used in extract_text().
        """
        os.utime(path, None)

    @classmethod
    def allowed_file(cls, filename) -> bool:
        """
        Prevents from filename injections or smth, flask docs recommend to do this.
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.allowed_extensions

    @classmethod
    def load_file(cls, request: Request) -> tuple:
        """
        Checks the file and secures it. Returns path to file and its extension.
        """
        if 'file' not in request.files:
            raise FileProcessingError(message="No file")
        file = request.files['file']
        if file.filename == '':
            raise FileProcessingError(message="No file selected")
        if file and FileService.allowed_file(file.filename):
            user_id = session['user_id'][0]
            filename = f"{user_id}_{secure_filename(file.filename)}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

            file.save(file_path)
            # safely update session list to track uploaded files without duplicates,
            # ensuring Flask detects the change by replacing the list in session.
            files = session.get('files', [])
            if filename not in files:
                files.append(filename)
                session['files'] = files

            extension = os.path.splitext(filename)[1].lower()
            return file_path, extension
        raise FileProcessingError(message="File type not allowed")
