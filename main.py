import discord
from discord.ext import commands
import os
import random
import json
import time
from dotenv import load_dotenv

# Global variables
cooldown = 0
status = ""
mod_roles = ""
triggers = {}
last_message_send_time = round(time.time() * 1000)

# Get cooldown and triggers from json
with open('config.json', 'r') as file:
    config = json.loads(file.read())
    cooldown = config["cooldown"] * 1000
    status = config["status"]
    mod_roles = config["mod_roles"]
    triggers = config["triggers"]

# Load token from .env
load_dotenv()
token = os.getenv('TOKEN')

# Initialize discord bot
intents = discord.Intents().all()
bot = commands.Bot(intents=intents, command_prefix='|', activity=discord.Game(name=status))

@bot.event
async def on_ready():
    print("{0.user} is online\n".format(bot))

@bot.event
async def on_message(message):
    global last_message_send_time

    if message.author == bot.user:
        return

    if message.content.startswith('!test'):
        for modRole in mod_roles:
            if modRole.lower() in [role.name.lower() for role in message.author.roles]:
                await message.channel.send(f'Hello {message.author.name}')
            else:
                print(getLocalTime(), "       ", message.author.name , " Has tried to access the command '!test'")

    current_time = round(time.time() * 1000)
    if current_time - last_message_send_time > cooldown:
        responses = None;
        words = message.content.lower().split()
        
        for word in triggers:
            if word in words:
                responses = triggers[word]

        if responses is not None:
            await message.channel.send(random.choice(responses))
            last_message_send_time = current_time

    await bot.process_commands(message)

@bot.command()
async def test(ctx):
    for modRole in mod_roles:
        if modRole.lower() in [role.name.lower() for role in ctx.message.author.roles]:
            await ctx.send(f'Hello {ctx.message.author.name}')
            return
            
    print(getLocalTime(), "       ", ctx.message.author.name , " Has tried to access the command '!test'")


def getLocalTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

bot.run(token)