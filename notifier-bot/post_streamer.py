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
        await asyncio.gather(*[self.run_watcher_stream(watcher, callback) for watcher in config.watchers])

    async def run_watcher_stream(self, watcher, callback):
        self.logger.info(f"Watcher \"{watcher['name']}\" started for r/{watcher['subreddit']}")
        subreddit = await self.reddit.subreddit(watcher["subreddit"])
        async for submission in subreddit.stream.submissions(skip_existing=True):
            if self.watcher_match(watcher, submission):
                asyncio.create_task(callback(Post(submission)))

    def watcher_match(self, watcher, submission):
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
    def __init__(self, submission):
        self.title = submission.title
        self.link = "https://reddit.com" + submission.permalink
        self.time = submission.created_utc
