import discord
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

token = config["Discord"]["token"]

client = discord.Client()

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
        brawlhalla_id = message.content.split(" ")[1]

client.run(token)
