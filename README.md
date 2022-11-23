# Discord Reddit Notifier
A bot for Discord that sends messages to a channel about new Reddit posts that match specific search terms.

I created this quickly when the [Pager app was down for 2 days](https://www.reddit.com/r/pager/comments/z07m7w/no_notifications/), so it's not exactly the most sophisticated bot. It currently only supports sending notifications to a single channel on a single server.

# Dependencies
This bot runs on Python 3.11 and depends on discord.py and aPRAW.

# Running the Bot
## Using Docker-Compose
1. Configure your settings in `./config/config.toml` [(Read more)](/docs/configuration.md)

2. Run docker-compose
    - `docker-compose up --build -d`

## Manual
1. Move `config.toml` from `config/` to `notifier-bot/`
    - `mv ./config/config.toml ./notifier-bot`

2. Change directory to `notifier-bot`
    - `cd notifier-bot`

3. Configure your settings in `config.toml`. [(Read more)](/docs/configuration.md)

4. Install required dependencies with `pip`
    - `pip install -r requirements.txt`

5. Run the bot
    - `python3 bot.py`