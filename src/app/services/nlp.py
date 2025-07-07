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
    Loads NLP models
    """
    models = {}

    @classmethod
    def load_all(cls):
        for lang, model_name in Config.nlp_models.items():
            try:
                cls.models[lang] = spacy.load(model_name, disable=['parser', 'ner'])
                log.info(f"Loaded model for: {lang}")
            except Exception as e:
                raise NLPException(exception=e)

    @classmethod
    def get(cls, lang: str):
        return cls.models.get(lang)
