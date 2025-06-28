import langid
import spacy
import base64
from flask import (
    current_app, session,
)
from wordcloud import WordCloud


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
        for lang, model_name in {
            "en": "en_core_web_sm",
            "ru": "ru_core_news_sm"
        }.items():
            try:
                cls.models[lang] = spacy.load(model_name, disable=['parser', 'ner'])
                print(f"[NLPModels] Loaded model for: {lang}")
            except Exception as e:
                print(f"[NLPModels] Failed to load model for: {lang}. {e}")

    @classmethod
    def get(cls, lang: str):
        return cls.models.get(lang)


class FunctionsService:
    """
    Contains methods for complex operations.
    """

    @classmethod
    def generate_word_cloud(cls) -> str:
        redis = current_app.extensions['redis_service']
        user_id: str = session['user_id']
        analysis_id: str = session['active_result']
        analysis_result: dict = redis.analysis_result_get(user_id, analysis_id)
        
        raw_words: list = analysis_result['lists']['words']
        word_list: list = [word for word in raw_words if len(word) >= 3]
        # generating word cloud in svg, coding it to bytes to transfer
        wc = (WordCloud(
            background_color='white',
            width=1000,
            height=1000,
        )
              .generate(" ".join(word_list)))
        svg = wc.to_svg()
        svg_str = base64.b64encode(svg.encode()).decode()

        return svg_str
    
    @classmethod
    def generate_lemmatization(cls) -> list:
        redis = current_app.extensions['redis_service']
        user_id: str = session['user_id']
        analysis_id: str = session['active_result']
        analysis_result: dict = redis.analysis_result_get(user_id, analysis_id)
        text = " ".join(analysis_result['lists']['words'])
        lang = detect_language(text)
        if lang != 'ru' or lang != 'en':
            return []
        nlp = NLPModels.get(lang)
        if not nlp:
            return []
        doc = nlp(text)
        return [t.lemma_ for t in doc if not t.is_punct and not t.is_space]
