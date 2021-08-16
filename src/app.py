import discord
from discord.ext.commands import Bot
import aiohttp
import asyncio
import datetime
import urllib

BOT_PREFIX = "!"
TOKEN = open("config.txt", 'r').read().replace("\n", '')
client = Bot(command_prefix = BOT_PREFIX)

# Remove default help command in favor of our own
client.remove_command('help')


@client.event
async def on_ready():
    print("Bot is ready to receive commands!")

async def get_deal_by_id(id):
    if not id:
        return None

    print(f"Search for deal by id {id}")
    url = f"http://www.cheapshark.com/api/1.0/deals?id={id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if not response.status == 200:
                print(f"CheapShark API failed for call to {url}")
                return None
            return await response.json()

async def get_game_by_id(id):
    if not id:
        return None

    print(f"Search for game by id {id}")
    url = f"http://www.cheapshark.com/api/1.0/games?id={id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if not response.status == 200:
                print(f"CheapShark API failed for call to {url}")
                return None
            return await response.json()
            

async def get_games_by_name(channel, name):
    if not name:
        return None

    print(f"Searching for games for name \"{name}\"")
    await channel.send(f"Finding (up to) the top 5 CheapShark results for \"{name}\"...")
    url = f"http://www.cheapshark.com/api/1.0/games?title={urllib.parse.quote(name)}&limit=5"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if not response.status == 200:
                print(f"CheapShark API failed for call to {url}")
                channel.send(f"Failed to retrieve CheapShark results for \"{name}\"")
                return None
            try:
                tasks = [parse_results(item) for item in await response.json()]
                message = ">>> "
                for task in asyncio.as_completed(tasks):
                    message += await task
                sent = await channel.send(content=message)
                await sent.edit(suppress=True)
            except Exception as ex:
                print(ex)
                await channel.send(f"Failed to retrieve CheapShark results for \"{name}\"")
                

async def parse_results(item):
    if not item:
        return None
    key = await get_game_by_id(item.get('gameID', None))
    info = key.get('info', None)
    if(info):
        title = info.get('title', None)

    cheapestPriceInfo = key.get('cheapestPriceEver', None)
    if(cheapestPriceInfo):
        cheapestPriceEver = cheapestPriceInfo.get('price', None)
        cheapestPriceDate = cheapestPriceInfo.get('date', None)
        cheapestPriceDate = datetime.datetime.fromtimestamp(cheapestPriceDate).strftime('%B %d, %Y')

    # result is already sorted by cheapest price first, so we'll just grab the cheapest item and return that.
    deals = key.get('deals', None)
    if(deals):
        deal = next(iter(deals), None)
        if(deal):
            dealID = deal.get('dealID', None)
            dealDetails = await get_deal_by_id(dealID)
            deal_link = f"https://www.cheapshark.com/redirect.php?dealID={dealID}"
            if(dealDetails):
                gameInfo = dealDetails.get('gameInfo', None)
                if(gameInfo):
                    dealPrice = gameInfo.get('salePrice')
                    retailPrice = gameInfo.get('retailPrice')

    return f"__**Title**: {title}__\n**Retail Price**: ${retailPrice}\n**Current Price**: ${dealPrice}\n**Link**: {deal_link}\n**Cheapest Ever**: ${cheapestPriceEver} on {cheapestPriceDate}\n\n" 
    

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