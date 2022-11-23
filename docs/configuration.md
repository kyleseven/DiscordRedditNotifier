# Configuration
## Bot Settings
```toml
[bot]
token = "Insert Token Here"
channel_id = 9999999999999999999
search_interval = 60
posts_per_search = 30
```
### `token`
Your Discord Bot token.

Create a new application on the [Discord Developer Portal](https://discord.com/developers/applications/), then create a new bot to receive a token. Add this bot to your server.

### `channel_id`
The channel ID of the channel you want notifications to be sent to. The bot must be added to the server where this channel is located.

You can retrieve this by enabling Developer Mode in Discord (Settings -> Advanced), then right click the desired channel and Copy ID.

### `search_interval`
Time (in seconds) of how often the bot will search for new posts.

### `posts_per_search`
How many new posts the bot will fetch for each watcher.

## Reddit API
```toml
[reddit]
client_id = "Insert Client ID Here"
client_secret = "Insert Client Secret Here"
user_agent = "Discord Reddit Notifier Bot"
```

Create a script for personal use on the [Reddit Applications page](https://www.reddit.com/prefs/apps).

### `client_id`
Client ID of your reddit script.

### `client_secret`
Client secret of your reddit script.

### `user_agent`
User Agent header that is sent to the Reddit API. This can be left as-is.

## Watchers
See [watchers.md](watchers.md)