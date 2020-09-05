import discord
import configparser
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
        await message.author.send('Hello ' + str(message.author) + ' ! \nTo get verified you need to post your Brawlhalla ID in here like that. \n```BrawlhallaID: "your ID"```')

    if message.content.startswith('BrawlhallaID: '):
        brawl_id = message.content.split(" ")[1]
        discord_id = message.author.id
        link_discord_to_brawl_id(discord_id, brawl_id)
        await message.channel.send('The verification was successful!')

    if message.content == '!rank':
        discord_id = message.author.id
        await message.channel.send(get_player_ranked_by_discord_id(discord_id)['rating'])
client.run(token)
