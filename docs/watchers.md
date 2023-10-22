# Configuring Watchers
A watcher will watch a subreddit's "new" feed for posts whose titles match specific criteria.

The included `config.toml` includes examples like the one below:
```toml
[[watchers]]
name = "K-Pop Updates"
subreddit = "kpop"
enabled = true
channel_id = 8888888888888888888
match_mode = "OR"
search_terms = [
  "loona",
  "dreamcatcher",
  "red velvet",
  "itzy",
  "le sserafim",
  "aespa",
  "heize",
  "stayc"
]
```
This watcher will watch r/kpop for new posts that contain ANY of the `search_terms` in the title.


To add a new watcher, create a new line with `[[watchers]]` and fill in the fields below.

## `name`
A name to give to your watcher.

## `subreddit`
The subreddit the watcher should watch.

## `enabled`
Boolean value to enable the watcher or not.

## `channel_id` (optional)
The channel id of the channel you want notifications from this watcher to be sent to. If not defined, then notifications will be sent to `default_channel_id` in the `[bot]` configuration.

## `match_mode`
How the watcher determines a match. This can be set to:
- `"OR"`
    - Will notify if the post contains **ANY** of the strings in `search_terms`
- `"AND"`
    - Will notify if the post contains **ALL** of the strings in `search_terms`
- `"ALL"`
    - Will notify of **ALL** new posts in the subreddit, regardless of `search_terms`

## `search_terms`
An array of strings to search for in each post. Case does not matter here, as all string matching in this program is *not* case-sensitive.