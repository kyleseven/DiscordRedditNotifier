# Configuration
## Bot Settings
```toml
[bot]
token = "Insert Token Here"
channel_id = 9999999999999999999
```
### `token`
Your Discord Bot token.

Create a new application on the [Discord Developer Portal](https://discord.com/developers/applications/), then create a new bot to receive a token. Add this bot to your server.

### `channel_id`
The channel ID of the channel you want notifications to be sent to. The bot must be added to the server where this channel is located.

You can retrieve this by enabling Developer Mode in Discord (Settings -> Advanced), then right click the desired channel and Copy ID.

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