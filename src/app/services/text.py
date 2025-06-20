import re
import string
import uuid

import docx
import PyPDF2
import textract

from src.app.services.file import FileService


class TextService:
    """
    Contains necessary methods related to text processing.
    """
    @classmethod
    def extract_text(cls, file_path: str, extension: str):
        """
        Uses suitable module to extract text from file.
        """
        FileService.touch(file_path)
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
