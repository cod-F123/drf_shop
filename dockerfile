FROM python:3.13-slim

ENV PYTHONWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY  ./requirements.txt /app/

RUN pip3 install --upgrade pip -i https://mirror-pypi.runflare.com/simple
RUN pip3 install -r requirements.txt -i https://mirror-pypi.runflare.com/simple

COPY ./core /app/
