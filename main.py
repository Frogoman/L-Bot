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
            await message.channel.send(random.choice(responses))
            last_message_send_time = current_time

    await bot.process_commands(message)

@bot.command()
async def test(ctx):
    for modRole in mod_roles:
        if modRole.lower() in [role.name.lower() for role in ctx.message.author.roles]:
            await ctx.send(f'Hello {ctx.message.author.name}')
            return

    logger.info("%s Has tried to access the 'test' command without the appropriate roles", ctx.message.author.name)

class TriggerSelectModify(View):
    selectArray = []
    for word in triggers:
        selectArray.append(discord.SelectOption(label = word))

    @discord.ui.select(
        placeholder = "Select a trigger to modify",
        options = selectArray
    )
    
    async def select_callback (self, interaction, select):
        phraseString = ""
        counter = 0

        embed = discord.Embed(title = "Change phrase", description = "Change phrase from the responses", color = discord.Color.dark_magenta())
        embed.set_author(name = f"{interaction.user.name}", icon_url = f"{interaction.user.display_avatar}")

        for word in triggers[select.values[0]]:
            counter += 1
            phraseString += str(counter) + "- " + word + "\n"

        embed.add_field(name = f"Phrases for {select.values[0]}", value = phraseString)

        view = PhraseSelect(select.values[0])

        await interaction.response.edit_message(embed = embed, view = view)

class PhraseSelect(View):
    selectArray = []
    select = []
    trigger = ""

    def __init__(self, triggerWord):
        self.selectArray = [discord.SelectOption(label = phrase) for phrase in triggers[triggerWord]] 
        self.trigger = triggerWord
        super().__init__()
        

        self.select = Select(
            placeholder = "Select a phrase to modify",
            options = self.selectArray
        )

        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback (self, interaction):
        self.select.disabled = True

        embed = discord.Embed(title = "Change phrase", description = "Send a message with the phrase you would like to add instead of the current one", color = discord.Color.dark_magenta())
        embed.set_author(name = f"{interaction.user.name}", icon_url = f"{interaction.user.display_avatar}")
        embed.add_field(name = "Current trigger:", value = self.trigger)
        embed.add_field(name = "Current phrase:", value = self.select.values[0])
        embed.set_footer(text = "To cancel, send 'Exit'")

        await interaction.response.edit_message(
            embed = embed,
            view = None
        )
        await ChangeJsonPhrase(self.trigger, self.select.values[0], interaction)

@bot.command()
async def cp(ctx):
    await changephrase(ctx)

@bot.command()
async def changephrase(ctx):
    for modRole in mod_roles:
        if modRole.lower() in [role.name.lower() for role in ctx.message.author.roles]:
            # Prepare embed for Triggers
            triggerString = ""
            counter = 0

            embed = discord.Embed(title = "Change phrase", description = "Change phrase from the responses", color = discord.Color.dark_magenta())
            embed.set_author(name = f"{ctx.message.author.name}", icon_url = f"{ctx.message.author.display_avatar}")
            
            for word in triggers:
                counter += 1
                triggerString += str(counter) + "- " + word + "\n"

            embed.add_field(name = "Triggers", value = triggerString)

            # Prepare option picker for Triggers
            view = TriggerSelectModify()

            # Send embed with option selector
            await ctx.send(embed = embed, view = view)

            return

    logger.info("%s Has tried to access the 'changephrase' command without the appropriate roles", ctx.message.author.name)

async def ChangeJsonPhrase(triggerInput, phraseInput, interactionInput):
    def check(m: discord.Message):
        return m.author.id == interactionInput.user.id and m.channel.id == interactionInput.channel.id 

    try:
        msg = await bot.wait_for('message', check = check, timeout = 60.0)
    except asyncio.TimeoutError: 
        await interactionInput.channel.send(f"You didn't send any phrase for 60 seconds...")
        logger.info(f"{interactionInput.user.name} timed out the change on the phrase '{phraseInput}' in the trigger '{triggerInput}'")
        return
    else:
        if msg.content.lower() == "exit":
            embed = discord.Embed(title = "Cancelled change", color = discord.Color.dark_magenta())
            embed.set_author(name = f"{interactionInput.user.name}", icon_url = f"{interactionInput.user.display_avatar}")
            embed.add_field(name = "Trigger:", value = triggerInput)
            embed.add_field(name = "Phrase:", value = phraseInput)

            await interactionInput.channel.send(embed = embed)
            
            logger.info(f"{interactionInput.user.name} cancelled the change on the phrase '{phraseInput}' in the trigger '{triggerInput}'")
            return
        else:
            with open("config.json", "r") as jsonFile:
                data = json.load(jsonFile)

            for phrase in data["triggers"][triggerInput]:
                if phrase == phraseInput:
                    data["triggers"][triggerInput][data["triggers"][triggerInput].index(phraseInput)] = msg.content

            with open("config.json", "w") as jsonFile:
                json.dump(data, jsonFile, indent=4)

            openConfig()

            embed = discord.Embed(title = "Changed phrase", color = discord.Color.dark_magenta())
            embed.set_author(name = f"{interactionInput.user.name}", icon_url = f"{interactionInput.user.display_avatar}")
            embed.add_field(name = "Current trigger:", value = triggerInput, inline = False)
            embed.add_field(name = "Old phrase:", value = phraseInput, inline = True)
            embed.add_field(name = "New phrase:", value = msg.content, inline = True)

            await interactionInput.channel.send(embed = embed)
            logger.info(f"{interactionInput.user.name} changed the phrase '{phraseInput}' to '{msg.content}' in the trigger '{triggerInput}'")
            return

bot.run(token)