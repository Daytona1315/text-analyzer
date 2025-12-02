import langid
import spacy

from src.app.utils.config import Config
from src.app.utils.custom_exceptions import NLPException
from src.app.utils.logging import log


def detect_language(text: str) -> str:
    lang, _ = langid.classify(text)
    return lang


class NLPModels:
    """
    Manages NLP models with Lazy Loading pattern.
    Models are loaded into memory only upon first request.
    """

    models = {}

    @classmethod
    def get(cls, lang: str):

        if lang not in cls.models:
            model_name = Config.nlp_models.get(lang)

            if not model_name:
                return None

            try:
                cls.models[lang] = spacy.load(model_name, disable=["parser"])
            except Exception as e:
                raise NLPException(exception=e)

        return cls.models[lang]
