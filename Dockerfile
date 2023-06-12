FROM python:3.11.3-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

RUN apt-get update && apt-get install -y sqlite3

RUN alembic upgrade head

RUN sqlite3 cafe.db < dump.sql

CMD uvicorn app.main:app --host 0.0.0.0 --reload
