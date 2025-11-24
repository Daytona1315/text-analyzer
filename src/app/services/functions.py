from wordcloud import WordCloud

from src.app.services.nlp import (
    detect_language,
    NLPModels,
)
from src.app.utils.custom_exceptions import (
    FunctionsException,
    NLPException,
)
from src.app.utils.config import Config


class FunctionsService:
    """
    Contains methods for complex operations.
    """

    def __init__(self, redis, user_id, analysis_result):
        self.redis = redis
        self.user_id = user_id
        self.analysis_result = analysis_result

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
            raise FunctionsException(exception=e)

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
