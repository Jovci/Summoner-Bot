import aiofiles
import json


def get_rank_url(rank):
    RANK_URL_MAP = {
        "Unranked": "https://static.wikia.nocookie.net/leagueoflegends/images/b/b0/League_of_Legends_icon_nav.png/revision/latest?cb=20201105141350",
        "IRON": "https://static.wikia.nocookie.net/leagueoflegends/images/f/fe/Season_2022_-_Iron.png/revision/latest?cb=20220105213520",
        "BRONZE": "https://static.wikia.nocookie.net/leagueoflegends/images/e/e9/Season_2022_-_Bronze.png/revision/latest?cb=20220105214225",
        "SILVER": "https://static.wikia.nocookie.net/leagueoflegends/images/4/44/Season_2022_-_Silver.png/revision/latest?cb=20220105214225",
        "GOLD": "https://static.wikia.nocookie.net/leagueoflegends/images/8/8d/Season_2022_-_Gold.png/revision/latest?cb=20220105214225",
        "PLATINUM": "https://static.wikia.nocookie.net/leagueoflegends/images/3/3b/Season_2022_-_Platinum.png/revision/latest?cb=20220105214225",
        "DIAMOND": "https://static.wikia.nocookie.net/leagueoflegends/images/e/ee/Season_2022_-_Diamond.png/revision/latest?cb=20220105214226",
        "MASTER": "https://static.wikia.nocookie.net/leagueoflegends/images/e/eb/Season_2022_-_Master.png/revision/latest?cb=20220105214311",
        "GRANDMASTER": "https://static.wikia.nocookie.net/leagueoflegends/images/f/fc/Season_2022_-_Grandmaster.png/revision/latest?cb=20220105214312",
        "CHALLENGER": "https://static.wikia.nocookie.net/leagueoflegends/images/0/02/Season_2022_-_Challenger.png/revision/latest?cb=20220105214312",
    }
    return RANK_URL_MAP.get(rank, "https://static.wikia.nocookie.net/leagueoflegends/images/b/b0/League_of_Legends_icon_nav.png/revision/latest?cb=20201105141350")  # Return a default URL if the rank is not found

def get_champion_icon_url(champions, champion_id):
    champion_name = champions.get(champion_id, "Unknown")
    return f"https://ddragon.leagueoflegends.com/cdn/14.10.1/img/champion/{champion_name}.png"



async def get_last_uploaded_index():
    try:
        async with aiofiles.open('last_uploaded_icon.json', mode='r') as f:
            data = await f.read()
            return json.loads(data).get('last_index', 0)
    except FileNotFoundError:
        return 0

async def set_last_uploaded_index(index):
    async with aiofiles.open('last_uploaded_icon.json', mode='w') as f:
        data = json.dumps({'last_index': index})
        await f.write(data)