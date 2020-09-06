import configparser

import discord
from discord.utils import get

from data_handler import get_player_ranked_by_discord_id, link_discord_to_brawl_id
from brawlhalla import BrawlhallaDataUpdater


config = configparser.ConfigParser()
config.read('config.ini')
token = config["Discord"]["token"]

client = discord.Client()


unverified = 'unverified'
verified = 'verified'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_member_join(member):
    unverified_role = get(member.guild.roles, name=unverified)
    await member.add_roles(unverified_role)
    print(f"{member} was given {unverified}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!verify':
        await message.channel.send('Hello ' + str(message.author) + ' ! \nTo get verified you need to post your Brawlhalla ID in here like that. \n'
                                                                   '```BrawlhallaID: "your ID"```')

    if message.content.startswith('BrawlhallaID: '):
        brawl_id = message.content.split(" ")[1]
        discord_id = message.author.id
        link_discord_to_brawl_id(discord_id, brawl_id)
        verified_role = get(message.author.guild.roles, name=verified)
        unverified_role = get(message.author.guild.roles, name=unverified)
        await message.author.remove_roles(unverified_role)
        await message.author.add_roles(verified_role)
        await message.channel.send('```The verification was successful!\nTo get your rank assigned to your Account wait about 15 Minutes and then type !rank.```')

    if message.content == '!rank':
        discord_id = message.author.id
        player_ranked_data = get_player_ranked_by_discord_id(discord_id)
        get_tier = player_ranked_data['tier']
        tier = get_tier.split(" ")[0]
        rank_role = get(message.author.guild.roles, name=tier)

        name = player_ranked_data['name']
        region = player_ranked_data['region']
        rating = player_ranked_data['rating']
        peak_rating = player_ranked_data['peak_rating']
        wins = player_ranked_data['wins']
        games = player_ranked_data['games']
        losses = games - wins
        win_percentage = wins / (wins + losses) * 100
        global_rank = player_ranked_data['global_rank']
        rounded_win_percentage = round(win_percentage)

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


if __name__ == '__main__':
    brawlhalla_data_updater = BrawlhallaDataUpdater()
    brawlhalla_data_updater.start()

    client.run(token)
