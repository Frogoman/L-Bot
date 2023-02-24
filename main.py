import discord
from discord.ext import commands
from discord.ui import Select, View
import os
import random
import json
import time
import logging
import asyncio
from dotenv import load_dotenv

# Global variables
cooldown = 0
status = ""
mod_roles = ""
triggers = {}
last_message_send_time = round(time.time() * 1000)
# Phrase

# Get cooldown and triggers from json
def openConfig():
    global config, cooldown, status, mod_roles, triggers

    with open('config.json', 'r') as file:
        config = json.loads(file.read())
        cooldown = config["cooldown"] * 1000
        status = config["status"]
        mod_roles = config["mod_roles"]
        triggers = config["triggers"]
openConfig()

# Load token from .env
load_dotenv()
token = os.getenv('TOKEN')

# Set up logger
logger = logging.getLogger('discord')
handler = logging.FileHandler(filename='l_bot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# logger.info("Test message")
# logger.critical("Test message")
# logger.error("Test message")
# logger.warning("Test message")

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
  
    current_time = round(time.time() * 1000)
    if current_time - last_message_send_time > cooldown:
        responses = None;
        words = message.content.lower().split()
        
        for word in triggers:
            if word.lower() == words[0]:
                responses = triggers[word]

        if responses is not None:
            repsonseMessage = random.choice(responses)
            logger.info("Sent " + repsonseMessage + " in " + str(message.channel.name) + " answering to " + str(message.author.name))
            await message.channel.send(random.choice(responses))
            last_message_send_time = current_time

    await bot.process_commands(message)

bot.run(token)