import io
import base64
from flask import (
    current_app, session,
)
from wordcloud import WordCloud


class FunctionsService:
    """
    Contains methods for complex operations.
    """

    @classmethod
    def generate_word_cloud(cls):
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
