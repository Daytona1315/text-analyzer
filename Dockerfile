FROM python:3.12-slim

ENV PYTHONPATH="/app/src"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN python -m pip install --upgrade pip==23.2.1

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y catdoc

RUN python -m spacy download en_core_web_sm && \
    python -m spacy download ru_core_news_sm

COPY . /app

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app", "--preload"]
