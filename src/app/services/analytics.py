import spacy
from flask import current_app, session
from wordcloud import WordCloud

from src.app.consts import SessionKeys
from src.app.services.nlp import (
    detect_language,
    NLPModels,
)
from src.app.utils.custom_exceptions import (
    NLPException,
    AnalyticsException,
    LangException,
)
from src.app.utils.config import Config
from src.app.utils.logging import log


class AnalyticsService:
    """
    Contains methods for complex operations.
    """

    def __init__(self, analysis_result: dict) -> None:
        self.analysis_result = analysis_result

    @classmethod
    def create_from_session(cls):
        redis_service = current_app.extensions["redis_service"]
        user_id = session.get(SessionKeys.USER_ID)
        analysis_id = session.get(SessionKeys.ACTIVE_ANALYSIS_ID)
        if not user_id or not analysis_id:
            raise AnalyticsException()
        analysis_result = redis_service.analysis_result_get(user_id, analysis_id)
        if not analysis_result:
            raise AnalyticsException()
        return cls(analysis_result)

    def generate_word_cloud(self) -> str:
        """
        Generates a word cloud.
        Tries to use NLP for smart filtering (lemmatization, POS tagging, stop words).
        Falls back to simple length filtering if NLP fails or language is unsupported.
        """
        text = self.analysis_result.get("text", "")
        clean_text = ""
        use_fallback = True

        if text:
            try:
                lang = detect_language(text)
                if lang in Config.nlp_langs:
                    nlp = NLPModels.get(lang)
                    if nlp:
                        use_fallback = False
                        if len(text) > Config.nlp_word_min_length:
                            text = text[: Config.nlp_word_min_length]
                        doc = nlp(text)
                        valid_pos = {"NOUN", "PROPN", "ADJ", "VERB"}
                        clean_words = [
                            token.lemma_
                            for token in doc
                            if not token.is_stop
                            and not token.is_punct
                            and token.pos_ in valid_pos
                            and len(token.lemma_) > Config.nlp_word_min_length
                        ]
                        clean_text = " ".join(clean_words)

            except Exception as e:
                log.warning(
                    f"NLP wordcloud failed: {e}. Falling back to simple method."
                )
                use_fallback = False

            if use_fallback or not clean_text.strip():
                raw_words = self.analysis_result["lists"]["words"]
                clean_text = " ".join(
                    [w for w in raw_words if len(w) > Config.nlp_word_min_length]
                )

            if not clean_text.strip():
                raise AnalyticsException(
                    message="Not enough words to generate wordcloud."
                )

            try:
                wc = WordCloud(
                    background_color="white",
                    width=800,
                    height=400,
                    max_words=100,
                    collocations=False,
                ).generate(clean_text)
                svg = wc.to_svg()
                return svg

            except Exception as e:
                raise AnalyticsException(exception=e)

        raise AnalyticsException()

    def generate_lemmatization(self) -> list:
        text = " ".join(self.analysis_result["lists"]["words"])
        lang = detect_language(text)
        if len(text) > Config.nlp_max_length:
            text = text[: Config.nlp_max_length]
        if lang not in Config.nlp_langs:
            raise NLPException(message="Language is undefined.")
        nlp = NLPModels.get(lang)
        if not nlp:
            raise NLPException()
        doc = nlp(text)
        try:
            return [t.lemma_ for t in doc if not t.is_punct and not t.is_space]
        except Exception as e:
            raise NLPException(exception=e)

    def generate_ner(self) -> str:

        text = self.analysis_result.get("text", "")
        if not text:
            raise AnalyticsException()

        if len(text) > Config.nlp_max_length:
            text = text[: Config.nlp_max_length]

        lang = detect_language(text)
        if lang not in Config.nlp_langs:
            raise LangException()

        nlp = NLPModels.get(lang)
        if not nlp:
            raise NLPException()
        if len(text) > 1000000:
            text = text[:1000000]

        doc = nlp(text)

        try:
            html = spacy.displacy.render(doc, style="ent", page=False)
            return html
        except Exception as e:
            log.error("ERROR WHILE NER: ", e)
            raise AnalyticsException()
