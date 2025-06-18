import os
import re
import string
import docx
import PyPDF2
import textract
from flask import (
    Request,
    current_app,
    session,
)
from werkzeug.utils import secure_filename

from src.app.utils.env_loader import allowed_extensions
from src.app.utils.custom_exception import FileProcessingError


def touch(path: str) -> None:
    """
    Refresh file's 'mtime' to current time to prevent cleanup.
    It is used in extract_text().
    """
    os.utime(path, None)


def allowed_file(filename) -> bool:
    """
    Prevents from filename injections or smth, flask docs recommend to do this.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def load_file(request: Request) -> tuple:
    """
    Checks the file and secures it. Returns path to file and its extension.
    """
    if 'file' not in request.files:
        raise FileProcessingError(message="No file")
    file = request.files['file']
    if file.filename == '':
        raise FileProcessingError(message="No file selected")
    if file and allowed_file(file.filename):
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


class TextService:
    """
    Contains necessary methods related to text processing.
    """
    @classmethod
    def extract_text(cls, file_path: str, extension: str):
        """
        Uses suitable module to extract text from file.
        """
        touch(file_path)
        match extension:
            case '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            case '.docx':
                doc = docx.Document(file_path)
                return '\n'.join(para.text for para in doc.paragraphs)
            case '.pdf':
                text = ''
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text += page.extract_text() or ''
                return text
            case '.doc':
                return textract.process(file_path).decode('utf-8')
            case _:
                return ''

    @classmethod
    def analyze_text(cls, text: str) -> dict:
        """
        Analyzes a text string to extract lists and counts of its components.

        Args:
            text: The input string to analyze.

        Returns:
            A dictionary with the analysis results.
        """

        # Find all sequences of letters (words).
        # This regex handles words with hyphens or apostrophes inside.
        words = re.findall(r'[a-zA-Zа-яА-ЯёЁ]+(?:[-’\'][a-zA-Zа-яА-ЯёЁ]+)*', text)
        # find all sequences of digits (numbers).
        numbers = re.findall(r'\d+', text)
        # find all standard punctuation characters.
        punctuation_chars = [char for char in text if char in string.punctuation]
        # count all whitespace characters (spaces, tabs, newlines).
        whitespace_count = len(re.findall(r'\s', text))
        # calculate non-whitespace character count.
        chars_no_spaces_count = len(text) - whitespace_count
        result = {
            'preview': text[:140] + '...' if len(text) > 140 else text,
            # core metrics of the text.
            'metrics': {
                'characters_no_whitespace': chars_no_spaces_count,
                'characters_with_whitespace': len(text),
                'words': len(words),
                'numbers': len(numbers),
                'punctuation': len(punctuation_chars),
                'whitespace': whitespace_count
            },
            # lists of found items.
            'lists': {
                'words': words,
                'numbers': numbers,
                'punctuation': punctuation_chars
            }
        }

        return result
