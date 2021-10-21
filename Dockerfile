FROM python:3.7.5-slim-stretch

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR app/

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install wait-for-it

COPY run.sh .
COPY src/timeout/log_listener.py .
COPY src/ src/
COPY tests/ tests/
