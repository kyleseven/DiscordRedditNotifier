FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /discordbot

# Sync dependencies
COPY ./pyproject.toml ./
RUN uv sync

# Copy bot source code
COPY ./notifier-bot ./notifier-bot

CMD ["uv", "run", "./notifier-bot/bot.py"]
