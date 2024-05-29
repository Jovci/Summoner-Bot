import discord
import json
import aiohttp
import asyncio
from discord.ext import commands

# Define the guild IDs
guild_ids = [
    "1245151855810445383",
    "1245151996236005426",
    "1245157194794668133",
    "1245157226386296883"
]

# Load the bot token from environment variables
bot_token = "BOT_KEY"

# Define the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Function to fetch champion data
async def fetch_champion_data():
    url = "https://ddragon.leagueoflegends.com/cdn/14.10.1/data/en_US/champion.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return {champion['id']: int(champion['key']) for champion in data['data'].values()}
            return None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    champions = await fetch_champion_data()
    if not champions:
        print("Failed to fetch champion data")
        await bot.close()
        return

    emoji_mappings = {}
    for guild_id in guild_ids:
        guild = bot.get_guild(int(guild_id))
        if not guild:
            print(f"Failed to get guild with ID: {guild_id}")
            continue
        for emoji in guild.emojis:
            champion_name = emoji.name.replace("champ_", "").capitalize()
            if champion_name in champions:
                emoji_mappings[champion_name] = {"id": emoji.id, "guild_id": guild_id}
    
    with open('emojis.json', 'w') as f:
        json.dump(emoji_mappings, f, indent=4)
    
    print("Emojis populated successfully")
    await bot.close()

bot.run(bot_token)
