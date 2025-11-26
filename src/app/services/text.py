import re
import string
import uuid
import subprocess
import docx
import PyPDF2
import compressed_rtf
from flask import (
    session,
    render_template,
)
from src.app.utils.custom_exceptions import TextAnalysisException
from src.app.utils.custom_exceptions import FileException


class TextService:
    """
    Contains necessary methods related to text processing.
    """

    @classmethod
    def provide_text_analysis(cls, text: str) -> str:
        from src.broker.tasks import analyze_text_task
        user_id: str = session["user_id"]
        task = analyze_text_task.delay(text, user_id)

        return render_template("partials/processing.html", task_id=task.id)

    @classmethod
    def extract_text(cls, file_path: str, extension: str) -> str:
        text: str = ""
        try:
            match extension.lower():
                case ".txt":
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()

                case ".docx":
                    doc = docx.Document(file_path)
                    text = "\n".join(p.text for p in doc.paragraphs)

                case ".pdf":
                    text = ""
                    with open(file_path, "rb") as f:
                        reader = PyPDF2.PdfReader(f)
                        for page in reader.pages:
                            page_text = page.extract_text() or ""
                            text += page_text

                case ".doc":
                    try:
                        output = subprocess.check_output(["catdoc", file_path])
                        text = output.decode("utf-8")
                    except subprocess.CalledProcessError as e:
                        raise FileException(exception=e)

                case ".rtf":
                    try:
                        with open(file_path, "rb") as f:
                            data = f.read()
                            text = compressed_rtf.decompress(data).decode(
                                "utf-8", errors="ignore"
                            )
                    except Exception as e:
                        raise FileException(exception=e)

                case _:
                    raise FileException(
                        status=422,
                        message=f"Unsupported file type: {extension}",
                    )

        except Exception as e:
            raise FileException(exception=e)

        if not text.strip():
            raise FileException(status=422, message="File is empty.")

        return text

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
