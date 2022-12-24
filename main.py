import discord
import os
import random
import json
import time
from dotenv import load_dotenv

# Global variables
cooldown = 0
status = ""
triggers = {}
last_message_send_time = round(time.time() * 1000)

# Get cooldown and triggers from json
with open('config.json', 'r') as file:
    config = json.loads(file.read())
    cooldown = config["cooldown"] * 1000
    status = config["status"]
    triggers = config["triggers"]

# Load token from .env
load_dotenv()
token = os.getenv('TOKEN')

# Initialize discord client
intents = discord.Intents().all()
client = discord.Client(intents=intents, activity=discord.Game(name=status))

@client.event
async def on_ready():
    print("{0.user} is online".format(client))

@client.event
async def on_message(message):
    global last_message_send_time

    if message.author == client.user:
        return

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

client.run(token)