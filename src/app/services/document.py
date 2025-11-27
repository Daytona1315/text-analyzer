import subprocess
import docx
import PyPDF2
import compressed_rtf

from src.app.utils.custom_exceptions import FileException


class DocumentService:
    """
    Service responsible for reading content from various file formats.
    """

    @classmethod
    def read_content(cls, file_path: str, extension: str) -> str:
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
