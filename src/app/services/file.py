import csv
import os

from flask import (
    Request,
    session,
)
from werkzeug.utils import secure_filename

from src.app.utils.config import Config
from src.app.utils.logging import logger
from src.app.utils.custom_exceptions import (
    BaseAppException,
    FileException,
    CSVWriteException,
)


class FileService:
    """
    Contains necessary methods related to files.
    """

    @classmethod
    def allowed_file(cls, filename) -> bool:
        """
        Prevents from filename injections or smth, flask docs recommend to do this.
        """
        try:
            return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in Config.allowed_extensions
        except Exception as e:
            logger.error(f"Something went wrong with {filename}: {e}")
            raise BaseAppException()

    @classmethod
    def load_file(cls, request: Request) -> tuple:
        """
        Checks the file and secures it. Returns (path, extension) or an error message.
        """
        if 'file' not in request.files:
            raise FileException(
                status_code=422,
                message="No file."
            )
        file = request.files['file']
        if file.filename == '':
            raise FileException(
                status_code=422,
                message="Filename is empty. Please, choose the correct file."
            )
        if file and FileService.allowed_file(file.filename):
            user_id: str = session['user_id']
            filename: str = f"{user_id}_{secure_filename(file.filename)}"
            file_path: str = Config.base_dir + '/' + Config.upload_folder + '/' + filename
            file.save(file_path)
            extension: str = os.path.splitext(filename)[1].lower()
            return file_path, extension
        raise FileException(
            status_code=422,
            message=f"Unsupported file type."
        )

    @classmethod
    def write_csv(cls, text: list) -> str:
        user_id: str = session['user_id']
        filename: str = f'{user_id}_file.csv'
        abs_path: str = os.path.join(Config.base_dir, Config.upload_folder, filename)
        try:
            with open(abs_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(text)
            return f'files/{filename}'
        except Exception as e:
            logger.error(f"Failed to write csv for {user_id}: {e}")
            raise CSVWriteException()
