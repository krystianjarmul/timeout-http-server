FROM python:3.7.5-slim-stretch

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install wait-for-it

RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src
COPY tests/ /tests/

WORKDIR src/
