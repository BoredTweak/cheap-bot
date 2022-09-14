import discord
from discord.ext.commands import Bot
import os

from cheapshark.queries import get_games_by_name

BOT_PREFIX = "!"

if(os.path.isfile('config.txt')):
    TOKEN = open("config.txt", 'r').read().replace("\n", '')
elif(os.getenv('BOTTOKEN')):
    TOKEN = os.getenv('BOTTOKEN')
else:
    raise ValueError('Unable to obtain discord bot token.')

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True

client = Bot(command_prefix = BOT_PREFIX, intents=intents)

# Remove default help command in favor of our own
client.remove_command('help')


@client.event
async def on_ready():
    print("Bot is ready to receive commands!")

#Commands

@client.command(pass_context=True, aliases = ['deals', 'Deals', 'DEALS'])
async def search(ctx, *title):
    channel = ctx.message.channel
    sep = ' '
    title = sep.join(title)
    if not title:
        await channel.send("Unable to determine search criteria. Please try again with a specific title. E.g. - `!searchgames Phasmophobia`")
    
    await get_games_by_name(channel, title) 

@client.command(pass_context=True, aliases = ['Help', 'HELP'])
async def help(ctx):
    help = "You have asked for help!\nThis discord bot is capable of requesting the best game deals from a Public API across multiple platforms.\nCommands:\n`!deals {game name}` - Sends results for the cheapest price now as well as the cheapest price ever for a given game title. Limited to the top 5 matches for game name."
    author = ctx.message.author
    channel = ctx.message.channel
    await channel.send(help) 

client.run(TOKEN, reconnect=True)