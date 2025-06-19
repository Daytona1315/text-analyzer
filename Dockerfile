FROM python:3.12-slim

ENV PYTHONPATH="/app/src"

WORKDIR /app

COPY requirements.txt /app/

RUN python -m pip install --upgrade pip==23.2.1

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
