import discord
import os
from dotenv import load_dotenv
from datetime import datetime
from api import fetch_summoner_data, fetch_league_data, fetch_puuid
from utils import get_rank_url

# Load environment variables
load_dotenv()

def setup_commands(bot):
    @bot.command()
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
        
        print(f"PUUID found: {puuid}")
        
        print(f"Fetching summoner data for PUUID: {puuid}")
        summoner_data = await fetch_summoner_data(puuid)
        
        if summoner_data:
            summoner_level = summoner_data["summonerLevel"]
            profile_icon_id = summoner_data["profileIconId"]
            encrypted_summoner_id = summoner_data["id"]

            print(f"Found summoner data: summonerLevel={summoner_level}, profileIconId={profile_icon_id}, encryptedSummonerId={encrypted_summoner_id}")

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
                thumbnail_url = "https://via.placeholder.com/100x100"  # Default URL if none is found

            embed = discord.Embed(
                title="Summoner Information",
                description="Information of searched user",
                colour=0x00b0f4,
                timestamp=datetime.now()
            )
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_image(url=f"https://ddragon.leagueoflegends.com/cdn/13.8.1/img/profileicon/{profile_icon_id}.png")
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
            embed.add_field(name="Name", value=name, inline=False)
            embed.add_field(name="Queue Type", value=queue_type, inline=True)
            embed.add_field(name="Level", value=summoner_level, inline=True)
            embed.add_field(name="Rank", value=rank, inline=True)

            await ctx.followup.send(embed=embed)
        else:
            print("Failed to retrieve summoner data")
            await ctx.followup.send("Failed to retrieve summoner data")
