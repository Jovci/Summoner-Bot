import discord
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BOT_KEY = os.getenv("BOT_KEY")
bot = discord.Bot()


@bot.command()
async def summoner(ctx, name: str = None):
    name = name or ctx.author.name
    url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={API_KEY}"
    print(f"Sending request to: {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                summonerLevel = data["summonerLevel"]
                profileIconId = data["profileIconId"]
                encryptedSummonerId = data["id"]
                print(
                    f"Found summoner data: summonerLevel={summonerLevel}, profileIconId={profileIconId}, encryptedSummonerId={encryptedSummonerId}"
                )
                second_url = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{encryptedSummonerId}?api_key={API_KEY}"
                print(f"Sending second API request to: {second_url}")
                async with session.get(second_url) as resp2:
                    if resp2.status == 200:
                        data = await resp2.json()
                        entries = data
                        print(f"Second API response data: {data}")
                        if entries:
                            for entry in entries:
                                if entry["queueType"] == "RANKED_SOLO_5x5":
                                    queueTypeSolo = "Solo/Duo"
                                    RankedSoloTier = entry["tier"]
                                    RankSoloTierRank = entry["rank"]
                                    solo_rank = RankedSoloTier + " " + RankSoloTierRank
                                    break
                                elif entry[
                                        "queueType"] == "RANKED_TFT_DOUBLE_UP":
                                    queueTypeSolo = "TFT Double Up"
                                    RankedSoloTier = entry["tier"]
                                    RankSoloTierRank = entry["rank"]
                                    solo_rank = RankedSoloTier + " " + RankSoloTierRank
                                    break
                                else:
                                    queueTypeSolo = "Unranked"
                                    RankedSoloTier = "Unranked"
                                    RankSoloTierRank = "N/A"
                                    solo_rank = RankedSoloTier + " " + RankSoloTierRank
                                    break
                        else:
                            queueTypeSolo = "Unranked"
                            RankedSoloTier = "Unranked"
                            RankSoloTierRank = "N/A"
                            solo_rank = RankedSoloTier + " " + RankSoloTierRank

                        RANK_URL_MAP = {
                            "Unranked":
                                "https://static.wikia.nocookie.net/leagueoflegends/images/b/b0/League_of_Legends_icon_nav.png/revision/latest?cb=20201105141350",
                            "IRON":
                                "https://static.wikia.nocookie.net/leagueoflegends/images/f/fe/Season_2022_-_Iron.png/revision/latest?cb=20220105213520",
                            "BRONZE":
                                "https://static.wikia.nocookie.net/leagueoflegends/images/e/e9/Season_2022_-_Bronze.png/revision/latest?cb=20220105214225",
                            "SILVER":
                                "https://static.wikia.nocookie.net/leagueoflegends/images/4/44/Season_2022_-_Silver.png/revision/latest?cb=20220105214225",
                            "GOLD":
                                "https://static.wikia.nocookie.net/leagueoflegends/images/8/8d/Season_2022_-_Gold.png/revision/latest?cb=20220105214225",
                            "PLATINUM":
                                "https://static.wikia.nocookie.net/leagueoflegends/images/3/3b/Season_2022_-_Platinum.png/revision/latest?cb=20220105214225",
                            "DIAMOND":
                                "https://static.wikia.nocookie.net/leagueoflegends/images/e/ee/Season_2022_-_Diamond.png/revision/latest?cb=20220105214226",
                            "MASTER":
                                "https://static.wikia.nocookie.net/leagueoflegends/images/e/eb/Season_2022_-_Master.png/revision/latest?cb=20220105214311",
                            "GRANDMASTER":
                                "https://static.wikia.nocookie.net/leagueoflegends/images/f/fc/Season_2022_-_Grandmaster.png/revision/latest?cb=20220105214312",
                            "CHALLENGER":
                                "https://static.wikia.nocookie.net/leagueoflegends/images/0/02/Season_2022_-_Challenger.png/revision/latest?cb=20220105214312",
                        }
                        thumbnail_url = RANK_URL_MAP.get(RankedSoloTier, " ")
                        embed = discord.Embed(title="Summoner Information", description="Information of searched user", \
                                url="https://via.placeholder.com/100x100", colour=discord.Colour.red())
                        embed.set_image(
                            url=
                            f"https://ddragon.leagueoflegends.com/cdn/13.8.1/img/profileicon/{profileIconId}.png"
                        )
                        embed.set_thumbnail(url=thumbnail_url)
                        embed.add_field(name="Name", value=name, inline=True)
                        embed.add_field(name="Queue Type",
                                        value=queueTypeSolo,
                                        inline=True)
                        embed.add_field(name="Level",
                                        value=summonerLevel,
                                        inline=True)
                        embed.add_field(name="Rank",
                                        value=solo_rank,
                                        inline=True)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("Failed to retrieve summoner league data"
                                      )
            else:
                await ctx.send("Failed to retrieve summoner data")


bot.run(os.getenv("BOT_KEY"))