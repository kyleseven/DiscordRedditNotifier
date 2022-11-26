import asyncio
import logging

import asyncpraw
from asyncpraw.exceptions import AsyncPRAWException

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
                async for submission in subreddit.stream.submissions(skip_existing=True):
                    if self.watcher_match(watcher, submission):
                        asyncio.create_task(callback(Post(submission)))
            except AsyncPRAWException as err:
                self.logger.critical(f"Exception in watcher \"{watcher['name']}\": {err}")
                self.logger.info(f"Restarting watcher \"{watcher['name']}\"...")
                await asyncio.sleep(5)
                continue

    def watcher_match(self, watcher, submission):
        """Takes a watcher and submission and returns a boolean representing whether or not the submission
        title matches the watcher's parameters.
        """
        match watcher["match_mode"]:
            case "OR":
                if any(term.casefold() in submission.title.casefold() for term in watcher["search_terms"]):
                    return True
            case "AND":
                if all(term.casefold() in submission.title.casefold() for term in watcher["search_terms"]):
                    return True
            case "ALL":
                return True

        return False


class Post:
    """Takes only the relevant data from a submission.
    """
    def __init__(self, submission):
        self.title = submission.title
        self.link = "https://reddit.com" + submission.permalink
        self.time = submission.created_utc
