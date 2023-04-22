import os
from dotenv import load_dotenv
import discord
from test_bot import TestableBot
import requests

# backend currently must be hosted locally
baseurl = 'http://127.0.0.1:8000/'

load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']

bot = TestableBot(intents=discord.Intents.all(), command_prefix='!')

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to the server")
    channel = bot.get_channel(1090771155163549796)
    await channel.send("Running")

@bot.command(name = 'create_task', help = 'Creates a task')
async def task_creation(ctx, *args):
    if not args:
        await ctx.send("No task name given")
        return

    title = " ".join(args)

    url = baseurl + f"task"
    response = requests.post(url=url, data={"title": title})
    
    if response.status_code == 201:
        await ctx.send(f"The task \"{title}\" has been created!")
    else:
        await ctx.send("An error occured when trying to create the task")
        

bot.run(TOKEN)