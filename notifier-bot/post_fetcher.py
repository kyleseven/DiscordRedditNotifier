import datetime
from collections import OrderedDict

import asyncpraw

import config


class PostFetcher:
    def __init__(self, last_time: int):
        self.last_time = last_time
        self.reddit = asyncpraw.Reddit(
            client_id=config.reddit_client_id,
            client_secret=config.reddit_client_secret,
            user_agent=config.reddit_user_agent
        )

    async def fetch_new(self):
        new_posts: list[Post] = []

        watchers = config.watchers
        # Go through each watcher
        for watcher in watchers:
            if not watcher["enabled"]:
                continue

            submission_list = []
            subreddit = await self.reddit.subreddit(watcher["subreddit"])
            # Get the last 30 posts from the subreddit's "new" feed
            async for submission in subreddit.new(limit=config.posts_per_search):
                submission_list.append(submission)

            new_submissions = []

            # Search submissions based on match mode and terms
            for submission in submission_list:
                match watcher["match_mode"]:
                    case "OR":
                        if any(term.casefold() in submission.title.casefold() for term in watcher["search_terms"]):
                            new_submissions.append(submission)
                    case "AND":
                        if all(term.casefold() in submission.title.casefold() for term in watcher["search_terms"]):
                            new_submissions.append(submission)
                    case "ALL":
                        new_submissions.append(submission)

            # Filter out submissions that have already been notified (submission time is before last check time)
            new_submissions[:] = [
                submission for submission in new_submissions if submission.created_utc >= self.last_time]

            # Filter duplicates
            new_submissions = list(OrderedDict.fromkeys(new_submissions))

            for submission in new_submissions:
                new_posts.append(Post(submission))

        self.last_time = int(round(datetime.datetime.now().timestamp()))

        return new_posts


class Post:
    def __init__(self, submission):
        self.title = submission.title
        self.link = "https://reddit.com" + submission.permalink
        self.time = submission.created_utc
