import discord
import os
import random
from dotenv import load_dotenv

triggers = {
    "squ": [
        "You are making me jealous...",
        "Did you know that she is a cat?",
        "Why are you talking to her?",
        "She knows everything...",
        "Stop! No touchy the space cat!",
        "Bubble tea! Hah! Why are you looking at me like that...",
        "Psst! She is busy!",
        "You know she can hear you, right?",
        "Her tail is so fluffy!!",
        "You know if you talk to her too much, I will tentacle you.",
        "Don't look at me... but we are out of coffee.",
        "I don't like that look in your eyes! Why do you need her?",
        "She will eat your face!"
    ],

    "squchan": [
        "You are making me jealous...",
        "Did you know that she is a cat?",
        "Why are you talking to her?",
        "She knows everything...",
        "Stop! No touchy the space cat!",
        "Bubble tea! Hah! Why are you looking at me like that...",
        "Psst! She is busy!",
        "You know she can hear you, right?",
        "Her tail is so fluffy!!",
        "You know if you talk to her too much, I will tentacle you.",
        "Don't look at me... but we are out of coffee.",
        "I don't like that look in your eyes! Why do you need her?",
        "She will eat your face!"
    ],

    "coffee" : [
        "Give me",
        "I want it"
    ],

    "l" : [
        "Music starto....",
        "Ĭ̴̈́ ̷̈́̌s̷̏̋e̶̐̿ȇ̶͑ ̶͇̏è̸̚v̶̇́ẹ̷̌r̷̊̓y̷̏́t̴̋̕ḧ̶͆ì̷̕n̵̪͝g̷͐̀",
        "I dont understand",
        "I don't like the moon. It's lonely.",
        "I am not really an octocat.",
        "I don't eat humans! Shy won't let me!",
        "I hunger.",
        "Why does everyone want to touch my tentacle?",
        "I dont understand",
        "Do you have a snack?",
        "No... I don't need an eyedrop.",
        "Earth is a strange place.",
        "I can look like anything... but too much of me scares people.",
        "Plants are beautiful... but Shy forgets to water them all the time.",
        "Can I help?",
        "I like to touch the coffee.",
        "Why are you persistent?",
        "She is way too into spooky stories... should I look scarier?",
        "I ate some spaghetti. It was nice and crunchy!",
        "Oh Nyo~",
        "I like watching movies! You can rewatch people move over and over and over and over... ah...",
        "Shy's hair smells nice, so I ate her shampoo. I hiccuped bubbles for a week!",
        "I don't feel homesick anymore. I am home.",
        "We don't actually have facehuggers on the station... at least I don't think so.",
        "-Hiccup- I ate a block of soap.",
        "Humans are so fragile...",
        "Never gonna give you up! Never gonna let you down! Never gonna let you touch my space cat...",
        "I did eat her safety skirt. I have no regrets. Please don't tell her...",
        "My name is Alheitrakzoth."
    ]
}

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

    words = message.content.lower().split()
    
    for word in triggers:
        if word in words:
            responses = triggers[word]

    if responses is not None:
        await message.channel.send(random.choice(responses))

client.run(token)