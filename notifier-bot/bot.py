import asyncio
import datetime
import logging

import discord
import validators
from post_streamer import Post, PostStreamer

import config

intents = discord.Intents.default()
client = discord.Client(
    intents=intents,
    activity=discord.Activity(
        type=discord.ActivityType.listening, name="Subreddits"
    )
)


@client.event
async def setup_hook():
    # Set up the post fetcher
    post_streamer = PostStreamer()
    asyncio.create_task(post_streamer.stream_new(notify))


@client.event
async def on_ready():
    logging.getLogger("discord.bot").info(f"Logged in as {client.user}")


async def notify(post: Post, channel_id: int):
    """Send a message to the channel_id about the given post.
    """
    channel = client.get_channel(channel_id)

    title = post.title
    if post.link_flair_text:
        flair = post.link_flair_text.strip("[]")
        if not post.title.startswith(f"[{flair}]"):
            title = f"[{flair}] {title}"

    if len(title) > 256:
        title = title[:253] + "..."

    embed = discord.Embed(
        title=title,
        url=post.comments_link,
        color=post.embed_color,
        timestamp=datetime.datetime.fromtimestamp(post.created_utc),
    ).set_footer(text=f"by u/{post.author}")

    author_name = f"r/{post.subreddit}"
    if post.subreddit_icon:
        embed.set_author(name=author_name, icon_url=post.subreddit_icon)
    else:
        embed.set_author(name=author_name)

    if validators.url(post.thumbnail):
        embed.set_thumbnail(url=post.thumbnail)

    if post.selftext:
        description = post.selftext[:509] + "..." if len(post.selftext) > 512 else post.selftext
        embed.description = description

    await channel.send(embed=embed)  # type: ignore


client.run(config.token)
