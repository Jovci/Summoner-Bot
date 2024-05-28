import discord
import os
from dotenv import load_dotenv
from commands import setup_commands

load_dotenv()

BOT_KEY = os.getenv("BOT_KEY")

if not BOT_KEY:
    raise ValueError("BOT_KEY environment variable is not set")

bot = discord.Bot()

setup_commands(bot)

bot.run(BOT_KEY)
