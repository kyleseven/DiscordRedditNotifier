import discord
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
async def on_ready():
    # Set up the post fetcher
    post_streamer = PostStreamer()
    await post_streamer.stream_new(notify)


async def notify(post: Post):
    """Send a message to the channel_id about the given post.
    """
    channel = client.get_channel(config.channel_id)
    await channel.send(f"__**{discord.utils.escape_markdown(post.title)}**__\n<{post.link}>")  # type: ignore


client.run(config.token)
