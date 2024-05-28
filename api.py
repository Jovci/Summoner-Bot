import aiohttp
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY environment variable is not set")

async def fetch_puuid(game_name, tagline):
    encoded_game_name = quote_plus(game_name)
    encoded_tagline = quote_plus(tagline)
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{encoded_game_name}/{encoded_tagline}?api_key={API_KEY}"
    print(f"Sending request to: {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("puuid")
            print(f"Failed to retrieve PUUID: status={resp.status}")
            return None

async def fetch_summoner_data(puuid):
    url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={API_KEY}"
    print(f"Sending request to: {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            print(f"Failed to retrieve summoner data: status={resp.status}")
            return None

async def fetch_league_data(encrypted_summoner_id):
    url = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{encrypted_summoner_id}?api_key={API_KEY}"
    print(f"Sending request to: {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            print(f"Failed to retrieve league data: status={resp.status}")
            return None
