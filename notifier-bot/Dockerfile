FROM python:3.11-alpine

WORKDIR /discordbot

# Install dependencies for pip requirements
RUN apk add build-base

# Install pip requirements
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot source code
COPY ./*.py ./

CMD ["python", "./bot.py"]
