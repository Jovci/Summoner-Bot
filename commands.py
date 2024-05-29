import discord
from dotenv import load_dotenv
from datetime import datetime
from api import fetch_summoner_data, fetch_league_data, fetch_puuid, fetch_livegame, fetch_champion_data
from utils import get_rank_url, get_champion_icon_url, get_last_uploaded_index, set_last_uploaded_index
import json
import aiohttp

# Load environment variables
load_dotenv()
with open('emojis.json', 'r') as f:
    emoji_mappings = json.load(f)

def setup_commands(bot):
    @bot.command(description="Retrieves Summoner's Information")
    async def summoner(ctx, name: str = None):
        if not name or '#' not in name:
            await ctx.respond("Please provide a valid summoner name and tagline in the format 'name#tagline'.")
            return
        
        await ctx.defer()  # Acknowledge the command right away
        
        game_name, tagline = name.split('#')
        print(f"Fetching PUUID for: {game_name}#{tagline}")

        puuid = await fetch_puuid(game_name, tagline)
        if not puuid:
            await ctx.followup.send("Failed to retrieve PUUID for the given summoner.")
            return
        
        print(f"PUUID found: {puuid} \n")
        
        print(f"Fetching summoner data for PUUID: {puuid}")
        summoner_data = await fetch_summoner_data(puuid)
        
        if summoner_data:
            summoner_level = summoner_data["summonerLevel"]
            profile_icon_id = summoner_data["profileIconId"]
            encrypted_summoner_id = summoner_data["id"]

            print(f"Found summoner data: summonerLevel={summoner_level}, profileIconId={profile_icon_id}, encryptedSummonerId={encrypted_summoner_id} \n")

            print(f"Fetching league data for encryptedSummonerId: {encrypted_summoner_id}")
            league_data = await fetch_league_data(encrypted_summoner_id)
            
            queue_type, rank, rank_tier = "Unranked", "Unranked", "N/A"
            if league_data:
                for entry in league_data:
                    if entry["queueType"] == "RANKED_SOLO_5x5":
                        queue_type = "Solo/Duo"
                        rank = entry["tier"] + " " + entry["rank"]
                        rank_tier = entry["tier"]
                        break
                    elif entry["queueType"] == "RANKED_TFT_DOUBLE_UP":
                        queue_type = "TFT Double Up"
                        rank = entry["tier"] + " " + entry["rank"]
                        rank_tier = entry["tier"]
                        break
            
            print(f"League data found: queueType={queue_type}, rank={rank}, rankTier={rank_tier}")
            thumbnail_url = get_rank_url(rank_tier)
            if not thumbnail_url:
                thumbnail_url = "https://static.wikia.nocookie.net/leagueoflegends/images/b/b0/League_of_Legends_icon_nav.png/revision/latest?cb=20201105141350"  # Default URL if none is found

            embed = discord.Embed(
                title="Summoner Information",
                description="Information of searched user",
                colour=0x00b0f4,
                timestamp=datetime.now()
            )
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_image(url=f"https://ddragon.leagueoflegends.com/cdn/14.1.1/img/profileicon/{profile_icon_id}.png")
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
            embed.add_field(name="Name", value=name, inline=False)
            embed.add_field(name="Queue Type", value=queue_type, inline=True)
            embed.add_field(name="Level", value=summoner_level, inline=True)
            embed.add_field(name="Rank", value=rank, inline=True)

            await ctx.followup.send(embed=embed)
        else:
            print("Failed to retrieve summoner data")
            await ctx.followup.send("Failed to retrieve summoner data")
    
    @bot.slash_command(description="Gets Live Match Information")
    async def getmatch(ctx, name: str):
        if not name or '#' not in name:
            await ctx.respond("Please provide a valid summoner name and tagline in the format 'name#tagline'.")
            return
        
        await ctx.defer()  # Acknowledge the command right away
        
        game_name, tagline = name.split('#')
        requested_summoner = f"{game_name}#{tagline}"
        print(f"Fetching PUUID for: {requested_summoner}")

        puuid = await fetch_puuid(game_name, tagline)
        if not puuid:
            await ctx.followup.send("Failed to retrieve PUUID for the given summoner.")
            return
        
        print(f"PUUID found: {puuid}")

        livegame = await fetch_livegame(puuid)
        if not livegame:
            await ctx.followup.send("Failed to retrieve live game data for the given summoner.")
            return
        
        # Fetch champion data
        champions = await fetch_champion_data()

        blue_team = [
            {
                "name": participant['riotId'],
                "championId": participant['championId'],
                "summonerId": participant['summonerId']
            }
            for participant in livegame['participants'] if participant['teamId'] == 100
        ]
        red_team = [
            {
                "name": participant['riotId'],
                "championId": participant['championId'],
                "summonerId": participant['summonerId']
            }
            for participant in livegame['participants'] if participant['teamId'] == 200
        ]

        async def fetch_rank(summoner_id):
            league_data = await fetch_league_data(summoner_id)
            for entry in league_data:
                if entry["queueType"] == "RANKED_SOLO_5x5":
                    return f"{entry['tier']} {entry['rank']}"
            return "Unranked"

        # Fetch ranks for all players
        for player in blue_team:
            player['rank'] = await fetch_rank(player['summonerId'])
        for player in red_team:
            player['rank'] = await fetch_rank(player['summonerId'])

        # Prepare embed message
        embed = discord.Embed(
            title=f"LIVE GAME - {requested_summoner}",
            colour=0x00ff11,
            timestamp=datetime.now()
        )

        def get_emoji(champion_name):
            emoji_info = emoji_mappings.get(champion_name, None)
            if emoji_info:
                return f"<:{champion_name.lower()}:{emoji_info['id']}>"
            return ""

        blue_team_names = "\n".join(
            f"{get_emoji(champions[player['championId']])} **{player['name']}**" if player['name'] == requested_summoner else f"{get_emoji(champions[player['championId']])} {player['name']}"
            for player in blue_team
        )
        red_team_names = "\n".join(
            f"{get_emoji(champions[player['championId']])} **{player['name']}**" if player['name'] == requested_summoner else f"{get_emoji(champions[player['championId']])} {player['name']}"
            for player in red_team
        )

        blue_team_ranks = "\n".join(player['rank'] for player in blue_team)
        red_team_ranks = "\n".join(player['rank'] for player in red_team)

        embed.add_field(name="Blue Team", value=blue_team_names, inline=True)
        embed.add_field(name="Ranks", value=blue_team_ranks, inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=False)  # Empty field for spacing
        embed.add_field(name="Red Team", value=red_team_names, inline=True)
        embed.add_field(name="Ranks", value=red_team_ranks, inline=True)

        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        
        await ctx.followup.send(embed=embed)