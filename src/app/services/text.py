import re
import string
import uuid
from flask import (
    session,
    render_template,
)
from src.app.consts import SessionKeys
from src.app.utils.custom_exceptions import TextAnalysisException


class TextService:
    """
    Contains necessary methods related to text processing.
    """

    @classmethod
    def provide_text_analysis(cls, text: str) -> str:
        from src.broker.tasks import analyze_text_task

        user_id: str = session[SessionKeys.USER_ID]
        task = analyze_text_task.delay(text, user_id)
        return render_template("partials/processing.html", task_id=task.id)

    @classmethod
    def analyze_text(cls, text: str):
        """
        Analyzes a text string to extract lists and counts of its components.

        """
        try:
            # Find all sequences of letters (words).
            # This regex handles words with hyphens or apostrophes inside.
            words = re.findall(r"[a-zA-Zа-яА-ЯёЁ]+(?:[-’\'][a-zA-Zа-яА-ЯёЁ]+)*", text)
            # find all sequences of digits (numbers).
            numbers = re.findall(r"\d+", text)
            # find all standard punctuation characters.
            punctuation_chars = [char for char in text if char in string.punctuation]
            # count all whitespace characters (spaces, tabs, newlines).
            whitespace_count = len(re.findall(r"\s", text))
            # calculate non-whitespace character count.
            chars_no_spaces_count = len(text) - whitespace_count
            result = {
                "id": str(uuid.uuid4()),
                "text": text,
                "short_preview": text[:40] + "..." if len(text) > 140 else text,
                "preview": text[:140] + "..." if len(text) > 140 else text,
                "metrics": {
                    "characters_no_whitespace": chars_no_spaces_count,
                    "characters_with_whitespace": len(text),
                    "words": len(words),
                    "numbers": len(numbers),
                    "punctuation": len(punctuation_chars),
                    "whitespace": whitespace_count,
                },
                "lists": {
                    "words": words,
                },
            }

            return result
        except Exception as e:
            raise TextAnalysisException(exception=e)
