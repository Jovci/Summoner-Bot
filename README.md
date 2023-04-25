# League of Legends Discord Bot
![preview](https://user-images.githubusercontent.com/70718127/234160915-ab658c05-5249-4d1b-a9f8-cc6f7827c5ad.jpg)

If you want you can personally host the bot just include your own riot api key and discord bot token.
I currently have the bot deployed on heroku as its always online and easier for people to use.
The bot uses slash builder commands so it will embed when typing /summoner compared to the usual !summoner or .summoner command style other bots use.

**What does this bot do?**
- The bot sends 2 API request to the public riot API based off the summoners username. In the first API request's data we store the summonerLevel, profileIconId, and encryptedSummonerId which will be used in the second request. For the second request we use the encryptedSummonerId to get the summoners rank data.
    
**Why is it a discord bot?**
- I orginally made the bot for friends to use. They wanted something easy to use and didnt want to go through the process of using websites like op.gg, u.gg, etc to see ranks. So I made it a discord bot that responds off the command /summoner [name]

**Will there be more commands?**
- Yes! I would like to add commands that include data about matches played, champions, and runes but currently the public riot API only allows certain data to be accessed. Im hoping with this bot ill accepted into their developer program to get access to more api features league of legends and valorant.

**Where do you get the icons for the ranks and profile icons?**
- I get the icons from the League of Legends fandom wiki (https://leagueoflegends.fandom.com/wiki/Rank_(League_of_Legends)#Season_2022)
- When new ranked icons gets released for the 2023 season I will be sure to include those. As for the profile icons I used riots Data Dragon API for the profile icons.

**Why isn't my profile icon showing?**
- Currently the profile icons are for latest verison 13.8.1. If its not showing then that icon used is above verison 13.8.1. 

**Why doesnt it show all my ranks.**
- Discord embeds are weird, I made it only shows the rank of the last ranked gamemode that you played. I didnt have enough embed add fields to go across and it became very cluttered if I did try to add more fields.