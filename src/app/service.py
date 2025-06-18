import os
import re
import string
import docx
import PyPDF2
import textract
from flask import (
    Request,
    current_app, session,
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
    def count_text(cls, text: str) -> dict:
        """
        Returns a dictionary with the lists of words, punctuation, numbers
        and their counts at the end of every list. For example:
        ['me', 'love', 'code', 3]
        """
        splitted = text.split()
        dictionary = {
            'preview': [],
            'symbols': [],
            'words': [],
            'punctuation': [],
            'numbers': []
        }
        for word in splitted:  # main cycle
            if not word:
                continue  # skipping blank strings
            if word.isdigit():
                dictionary['numbers'].append(word)
            elif word and re.match(f'[{re.escape(string.punctuation)}]$', word[-1]):
                dictionary['punctuation'].append(word[-1])
                w = word[:-1]
                if w:  # if the part of word remained
                    if w.isdigit():
                        dictionary['numbers'].append(w)
                    else:
                        dictionary['words'].append(w)
            else:
                dictionary['words'].append(word)
        for symbol in text.strip():  # counting symbols
            if symbol == " " or symbol == "/n":
                continue
            else:
                dictionary['symbols'].append(symbol)
        for key in dictionary:  # adding quantity of each category to the end of every list
            count = len(dictionary[key])
            dictionary[key].append(count if count > 0 else 0)
        spaces: int = text.count(" ")  # counting spaces
        dictionary['spaces'] = [spaces if spaces > 0 else 0]
        preview: str = text[:140]  # adding preview string
        dictionary['preview'] = [preview]
        return dictionary
