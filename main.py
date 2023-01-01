import discord
import os
import random
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents().all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("{0.user} is online".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    username = str(message.author).split("#")[0]
    user_message = str(message.content.strip())

    if user_message.lower().startswith("squ ") or user_message.lower().startswith("squchan ") or user_message.lower() == "squ" or user_message.lower() == "squchan":
        with open("responses-l.txt",encoding="utf8") as f:
            Responses_Squ = f.readlines()
        await message.channel.send(random.choice(Responses_Squ))
    elif user_message.lower().startswith("l ") or user_message.lower() == "l":
        with open("responses-l.txt",encoding="utf8") as f:
            L_Response = f.readlines()
        await message.channel.send(random.choice(L_Response))
    elif user_message.lower().startswith("coffee ") or user_message.lower() == "coffee":
        with open("responses-coffee.txt",encoding="utf8") as f:
            Responses_Coffee = f.readlines()
        await message.channel.send(random.choice(Responses_Coffee))


client.run(token)   