import configparser
import time

import discord
from discord.utils import get

from data_handler import *

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
    if unverified_role is not None:
        await member.add_roles(unverified_role)

    time.sleep(5)
    verified_channel_id = int(config["Discord"]["verify_channel"])
    verified_channel = member.guild.get_channel(verified_channel_id)
    if verified_channel is not None:
        await verified_channel.send("Hello {}.\n"
                                    "Welcome to the Mysticis Server\n"
                                    "To get verified use ```!verify <your-brawlhalla-id>```".format(member.mention))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!verify'):
        cmd = message.content.split()
        if len(cmd) == 1:
            await message.channel.send('To get verified you need to post your Brawlhalla ID in here like that. \n'
                                       '```!verify <your_brawlhalla_id>```')
        else:
            try:
                brawl_id = int(cmd[1])
            except ValueError:
                await message.channel.send("Sorry, {} is not a valid id".format(cmd[1]))
                return

            discord_id = message.author.id
            link_discord_to_brawl_id(discord_id, brawl_id)
            verified_role = get(message.author.guild.roles, name=verified)
            unverified_role = get(message.author.guild.roles, name=unverified)
            if unverified_role is not None:
                await message.author.remove_roles(unverified_role)
            if verified_role is not None:
                await message.author.add_roles(verified_role)
            await message.channel.send(
                '```The verification was successful!\nTo get your rank assigned to your Account wait about 15 Minutes and then type !rank.```')

    if message.content.startswith('!rank'):
        cmd = message.content.split()
        if len(cmd) == 1:
            discord_id = message.author.id
        elif cmd[1].startswith('<@!') and cmd[1].endswith('>'):
            # The user mentioned somebody
            discord_id = cmd[1][3:-1]
        else:
            await message.channel.send(
                'Sorry, {} is not a valid user. Use either a mention (!rank @username) or just !rank to get your own ranked info.'.format(
                    cmd[1]))
            return

        player_ranked_data = get_player_ranked_by_discord_id(discord_id)
        if player_ranked_data is None:
            await message.channel.send("Sorry, I don't have your ranked data yet. Come back in a few minutes.")
            return

        get_tier = player_ranked_data['tier']
        tier = get_tier.split(" ")[0]
        rank_role = get(message.author.guild.roles, name=tier)
        if rank_role is not None:
            await message.author.add_roles(rank_role)

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

        await message.channel.send('```Player Data'
                                   '\n\nName\t\t\t\t\t\t\t\tRegion\n'
                                   + str(name) + '\t\t\t\t' + str(region) + '\n\n'
                                                                            '\t\t\t\t\tRanked Data\n\n'
                                                                            '\t\t\t\t\t1v1 Ranking\n\t\t\t\t\t'
                                   + str(get_tier) + '\n\t\t\t\t\t'
                                                     '(' + str(rating) + ' / ' + str(peak_rating) + ' Peak)\n\t\t\t\t\t'
                                   + str(wins) + ' Wins / ' + str(losses) + ' Losses\n\t\t\t\t\t'
                                                                            '(Total Games ' + str(
            games) + ')\n\t\t\t\t\t'
                                   + str(rounded_win_percentage) + '% Winrate\n\t\t\t\t\t'
                                                                   'Global Rank ' + str(global_rank) + '```')


    if message.content == "!clan Mysticis":

        mysticis_channel_id = int(config["Discord"]["mysticis_channel"])
        mysticis_channel = message.author.guild.get_channel(mysticis_channel_id)
        clan_role = get(message.author.guild.roles, name="Mysticis")

        if mysticis_channel_id is not None:
            mysticis_role_id = config.getint("Discord", "clan_role_ids")
            discord_ids = [str(user.id) for user in message.guild.get_role(mysticis_role_id).members]

            for mysticis_player in discord_ids:
                mysticis_player_stats = get_player_stats_by_discord_id(mysticis_player)
                mysticis_player_rank_stats = get_player_ranked_by_discord_id(mysticis_player)
                name = mysticis_player_rank_stats['name']
                rank = mysticis_player_rank_stats['rating']
                monthly_xp = 123
                xp_overall = mysticis_player_stats['clan']['personal_xp']

                await mysticis_channel.send("```Name: "+str(name)+"\n"
                                          "Elo: "+str(rank)+"\n"
                                          "Monthly xp gain: "+str(monthly_xp)+"/7000\n"
                                          "Xp overall: "+str(xp_overall)+"\n```")

    if message.content.startswith("!brawldb"):
        cmd = message.content.split()
        if len(cmd) == 1:
            discord_id = message.author.id
        else:
            if cmd[1].startswith('<@!') and cmd[1].endswith('>'):
                # The user mentioned somebody
                discord_id = cmd[1][3:-1]
            else:
                discord_id = cmd[1]
            try:
                discord_id = int(discord_id)
            except ValueError:
                await message.channel.send("Sorry, {} is not a valid mention or a user id!".format(discord_id))
                return

        brawl_id = get_brawl_id_by_discord_id(discord_id)
        if brawl_id is None:
            await message.channel.send("Sorry, <@!{}> is not yet verified!".format(discord_id))
            return
        await message.channel.send("https://brawldb.com/player/stats/{}".format(brawl_id))


    if message.content == "!test":
        discord_id = message.author.id
        await message.channel.send(get_player_ranked_by_discord_id(discord_id)['tier'])

if __name__ == '__main__':
    client.run(token)
