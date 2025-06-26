import re
import string
import uuid
import subprocess
import docx
import PyPDF2
import compressed_rtf
from flask import (
    Response,
    session,
    current_app,
    render_template,
    make_response,
)

from app.utils.custom_exceptions import FileIsEmpty


class TextService:
    """
    Contains necessary methods related to text processing.
    """

    @classmethod
    def provide_text_analysis(cls, text: str) -> Response:
        user_id: str = session['user_id']
        redis = current_app.extensions['redis_service']
        result = TextService.analyze_text(text)
        redis.analysis_result_save(user_id, result)
        result_html = render_template('partials/result.html', result=result)
        response = make_response(result_html)
        response.headers['HX-Trigger'] = 'historyNeedsUpdate'
        # adding current result in session for further operations
        session['active_result'] = result['id']
        return response

    @classmethod
    def extract_text(cls, file_path: str, extension: str):
        match extension.lower():
            case '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            case '.docx':
                doc = docx.Document(file_path)
                return '\n'.join(p.text for p in doc.paragraphs)
            case '.pdf':
                text = ''
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text += page.extract_text() or ''
                return text
            case '.doc':
                try:
                    output = subprocess.check_output(['catdoc', file_path])
                    return output.decode('utf-8')
                except Exception:
                    return ''
            case '.rtf':
                try:
                    with open(file_path, 'rb') as f:
                        data = f.read()
                        return compressed_rtf.decompress(data).decode('utf-8', errors='ignore')
                except Exception:
                    return ''
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
            'id': str(uuid.uuid4()),
            'short_preview': text[:40] + '...' if len(text) > 140 else text,
            'preview': text[:140] + '...' if len(text) > 140 else text,
            'metrics': {
                'characters_no_whitespace': chars_no_spaces_count,
                'characters_with_whitespace': len(text),
                'words': len(words),
                'numbers': len(numbers),
                'punctuation': len(punctuation_chars),
                'whitespace': whitespace_count
            },
            'lists': {
                'words': words,
            }
        }

        return result
