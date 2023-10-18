FROM python:latest

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY . .

RUN chmod +x ./app-entry-point.sh