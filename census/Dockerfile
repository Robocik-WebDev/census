FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y build-essential netcat libpq-dev
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

