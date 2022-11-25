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

post_fetcher: PostStreamer


@client.event
async def on_ready():
    # Set up the post fetcher
    global post_fetcher
    post_fetcher = PostStreamer()
    await post_fetcher.stream_new(notify)


async def notify(post: Post):
    channel = client.get_channel(config.channel_id)
    await channel.send(f"__**{post.title}**__\n<{post.link}>")  # type: ignore


client.run(config.token)
