FROM python:3.11-alpine

WORKDIR /discordbot

COPY ./requirements.txt ./
COPY ./*.py ./

RUN apk add build-base

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./bot.py"]
