import asyncio
import logging

import asyncpraw

import config


class PostStreamer:
    def __init__(self):
        self.logger = logging.getLogger("discord.post_streamer")
        self.reddit = asyncpraw.Reddit(
            client_id=config.reddit_client_id,
            client_secret=config.reddit_client_secret,
            user_agent=config.reddit_user_agent
        )

    async def stream_new(self, callback):
        """Runs all of the subreddit streams for each enabled watcher. Callback is passed to run_watcher_stream()
        """
        enabled_watchers = [watcher for watcher in config.watchers if watcher["enabled"]]
        await asyncio.gather(*[self.run_watcher_stream(watcher, callback) for watcher in enabled_watchers])

    async def run_watcher_stream(self, watcher, callback):
        """Runs a subreddit stream for the given watcher and performs the callback when a matching
        submission is found.
        """
        while True:
            self.logger.info(f"Watcher \"{watcher['name']}\" started for r/{watcher['subreddit']}")
            try:
                subreddit = await self.reddit.subreddit(watcher["subreddit"])
                await subreddit.load()

                subreddit_icon = subreddit.icon_img
                watcher_color = watcher.get("color", config.default_color)
                channel_id = watcher.get("channel_id", config.default_channel_id)

                async for submission in subreddit.stream.submissions(skip_existing=True):
                    if self.watcher_match(watcher, submission):
                        asyncio.create_task(callback(Post(submission, subreddit_icon, watcher_color), channel_id))
            except Exception as err:
                self.logger.warning(f"{type(err).__name__} caught in watcher \"{watcher['name']}\". Restarting...")
                await asyncio.sleep(5)
                continue

    @staticmethod
    def watcher_match(watcher, submission):
        """Determines if the submission title matches the watcher's parameters.
        This is a case-insensitive comparison.
        """
        title = submission.title.casefold()
        search_terms = [term.casefold() for term in watcher["search_terms"]]

        match watcher["match_mode"]:
            case "OR":
                return any(term in title for term in search_terms)
            case "AND":
                return all(term in title for term in search_terms)
            case "ALL":
                return True

        return False


class Post:
    """Takes only the relevant data from a submission.
    """
    def __init__(self, submission, subreddit_icon, embed_color):
        self.title = submission.title
        self.author = submission.author
        self.subreddit = submission.subreddit
        self.created_utc = submission.created_utc
        self.is_self = submission.is_self
        self.selftext = submission.selftext
        self.thumbnail = submission.thumbnail
        self.link_flair_text = submission.link_flair_text
        self.comments_link = "https://reddit.com" + submission.permalink
        self.subreddit_icon = subreddit_icon
        self.embed_color = embed_color
