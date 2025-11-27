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
)
from src.app.utils.config import Config


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
        raw_words: list = self.analysis_result["lists"]["words"]
        word_list: list = [word for word in raw_words if len(word) >= 3]
        # generating word cloud in svg, coding it to bytes to transfer
        try:
            wc = WordCloud(
                background_color="white",
                width=1000,
                height=1000,
            ).generate(" ".join(word_list))
            svg = wc.to_svg()
            return svg
        except Exception as e:
            raise AnalyticsException(exception=e)

    def generate_lemmatization(self) -> list:
        text = " ".join(self.analysis_result["lists"]["words"])
        lang = detect_language(text)
        if lang not in Config.nlp_langs:
            raise NLPException(message="Language is undefined. Try longer text.")
        nlp = NLPModels.get(lang)
        if not nlp:
            raise NLPException()
        doc = nlp(text)
        try:
            return [t.lemma_ for t in doc if not t.is_punct and not t.is_space]
        except Exception as e:
            raise NLPException(exception=e)
