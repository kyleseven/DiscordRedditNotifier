import datetime

import discord
from discord.ext import tasks

import config
from post_fetcher import PostFetcher

intents = discord.Intents.default()
client = discord.Client(intents=intents)

post_fetcher: PostFetcher


@client.event
async def on_ready():
    # Set up the post fetcher
    global post_fetcher
    post_fetcher = PostFetcher(int(round(datetime.datetime.now().timestamp())))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Reddit Threads"))
    # Start looping task
    notify.start()


@tasks.loop(seconds=config.search_interval)
async def notify():
    global post_fetcher
    new_posts = await post_fetcher.fetch_new()
    channel = client.get_channel(config.channel_id)
    for post in new_posts:
        await channel.send(f"__**{post.title}**__\n<{post.link}>")  # type: ignore


client.run(config.token)
