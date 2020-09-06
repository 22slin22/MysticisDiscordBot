import configparser

import discord
from discord import Embed
from discord.utils import get

from data_handler import get_player_ranked_by_discord_id, link_discord_to_brawl_id
from brawlhalla import BrawlhallaDataUpdater

config = configparser.ConfigParser()
config.read('config.ini')

token = config["Discord"]["token"]

client = discord.Client()

brawlhalla_data_updater = BrawlhallaDataUpdater()
brawlhalla_data_updater.start()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!verify':
        await message.author.send('Hello ' + str(message.author) + ' ! \nTo get verified you need to post your Brawlhalla ID in here like that. \n'
                                                                   '```BrawlhallaID: "your ID"```')

    if message.content.startswith('BrawlhallaID: '):
        brawl_id = message.content.split(" ")[1]
        discord_id = message.author.id
        link_discord_to_brawl_id(discord_id, brawl_id)
        await message.channel.send('The verification was successful!')

    if message.content == '!rank':
        discord_id = message.author.id
        get_tier = get_player_ranked_by_discord_id(discord_id)['tier']
        tier = get_tier.split(" ")[0]
        rank_role = get(message.author.guild.roles, name=tier)
        name = get_player_ranked_by_discord_id(discord_id)['name']
        region = get_player_ranked_by_discord_id(discord_id)['region']
        rating = get_player_ranked_by_discord_id(discord_id)['rating']
        peak_rating = get_player_ranked_by_discord_id(discord_id)['peak_rating']
        wins = get_player_ranked_by_discord_id(discord_id)['wins']
        games = get_player_ranked_by_discord_id(discord_id)['games']
        losses = games - wins
        win_perecentage = wins / (wins + losses) * 100
        global_rank = get_player_ranked_by_discord_id(discord_id)['global_rank']
        rounded_win_percentage = round(win_perecentage)
        await message.author.add_roles(rank_role)
        await message.channel.send('```Player Data'
                                   '\n\nName\t\t\t\t\t\t\t\tRegion\n'
                                   + str(name) + '\t\t\t\t' + str(region) + '\n\n'
                                   '\t\t\t\t\tRanked Data\n\n'
                                   '\t\t\t\t\t1v1 Ranking\n\t\t\t\t\t'
                                   + str(get_tier) + '\n\t\t\t\t\t'
                                   '(' + str(rating) + ' / ' + str(peak_rating) + ' Peak)\n\t\t\t\t\t'
                                   + str(wins) + ' Wins / ' + str(losses) + ' Losses\n\t\t\t\t\t'
                                   '(Total Games ' + str(games) + ')\n\t\t\t\t\t'
                                   + str(rounded_win_percentage) + '% Winrate\n\t\t\t\t\t'
                                   'Global Rank ' + str(global_rank) + '```')

    if message.content == "!test":
        discord_id = message.author.id
        await message.channel.send(get_player_ranked_by_discord_id(discord_id)['tier'])
client.run(token)
