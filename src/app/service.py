import os
import re
import string
import docx
import PyPDF2
import textract
from flask import (
    Request,
    render_template,
    current_app,
)
from werkzeug.utils import secure_filename

from src.app.main import allowed_extensions


def allowed_file(filename) -> bool:
    """
    Prevents from filename injections or smth, flask docs recommends to do this.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def load_file(request: Request) -> tuple:
    """
    Checks the file and secures it. Returns path to file and its extension.
    """
    if 'file' not in request.files:
        return render_template('partials/error.html')
    file = request.files['file']
    if file.filename == '':
        print('No selected file')
        return render_template('partials/error.html')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        extension = os.path.splitext(filename)[1].lower()
        return file_path, extension
    return render_template('partials/error.html')


class TextService:
    """
    Contains necessary methods.
    """
    @classmethod
    def extract_text(cls, file_path: str, extension: str):
        """
        Uses suitable module to extract text from file.
        """
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
        Returns a dictionary with words, punctuation, numbers lists and their counts at the end.
        """
        splitted = text.split()
        dictionary = {
            'preview': [],
            'symbols': [],
            'words': [],
            'punctuation': [],
            'numbers': []
        }
        # Main cycle
        for word in splitted:
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
        # Counting symbols
        for symbol in text.strip():
            if symbol == " " or symbol == "/n":
                continue
            else:
                dictionary['symbols'].append(symbol)
        # Adding quantity of each category to the end of every list
        for key in dictionary:
            count = len(dictionary[key])
            dictionary[key].append(count if count > 0 else 0)
        # Counting spaces
        spaces: int = text.count(" ")
        dictionary['spaces'] = [spaces if spaces > 0 else 0]
        # Adding preview string
        preview = text[:170]
        dictionary['preview'] = preview

        return dictionary
