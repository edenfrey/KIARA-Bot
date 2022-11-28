"""
KIARA Discord Bot Base Code
Author: Amir Adrian Amir Hamzah
Description: This is the base code that creates an instance of the bot which can be activated and hosted locally to bring the respective bot online

"""
import os

# Import Libraries
import discord
from dotenv import load_dotenv

# Extract Private Credentials
load_dotenv()
BOT_TOKEN = os.getenv("bot_token")

# Activate Bot
intents = discord.Intents.all()
client = discord.Client(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("KIARA?"):
        await message.channel.send("I am here!")


client.run(BOT_TOKEN)

# Bot Passive Behavior


# Bot Active Behavior


# Bot Commanded Behavior
