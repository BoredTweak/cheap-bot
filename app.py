import discord
from discord.ext.commands import Bot
import requests
import datetime
import csv
import time

BOT_PREFIX = "!"
TOKEN = open("config.txt", 'r').read().replace("\n", '')
client = Bot(command_prefix = BOT_PREFIX)

# Remove default help command in favor of our own
client.remove_command('help')


@client.event
async def on_ready():
    print("Bot is ready to receive commands!")


def get_deal_by_id(id):
    print("Search for deals for id " + id)
    url = "http://www.cheapshark.com/api/1.0/deals?id="+id
    response = requests.get(url)
    data = response.json()
    return data

def get_game_by_id(id):
    url = "http://www.cheapshark.com/api/1.0/games?id="+id
    response = requests.get(url)
    data = response.json()
    return data


def get_games_by_name(name):
    result = []
    url = "http://www.cheapshark.com/api/1.0/games?title="+name+"&limit=5"
    response = requests.get(url)
    data = response.json()
    for item in data:
        result.append(get_game_by_id(item["gameID"]))
    return result

async def parse_games(channel, data):
    print("Parsing Games")
    print(data)
    game_list = []
    stores = []
    ids = []

    for key in data:
        print()
        print(key)
        game = {}
        game['title'] = key['info']['title']
        game['picture'] = key['info']['thumb']
        game['cheapestPriceEver'] = key['cheapestPriceEver']['price']
        game['cheapestPriceDate'] = datetime.datetime.fromtimestamp(key['cheapestPriceEver']['date']).strftime('%d-%b-%Y')
        deals = []
        # result is already sorted by cheapest price first, so we'll just grab the cheapest item and return that.
        for deal in key['deals'][:1]:
            dealID = deal['dealID']
            dealDetails = get_deal_by_id(dealID)
            deal_link = "https://www.cheapshark.com/redirect.php?dealID=" + dealID
            game['dealPrice'] = dealDetails['gameInfo']['salePrice']
            game['dealLink'] = deal_link

        game_list.append(game)
        await channel.send(game['title'] + " is currently cheapest at " + game['dealLink'] + " for the price of $" + game['dealPrice'] + ". It was cheapest ever at $" + game['cheapestPriceEver'] + " on " + game['cheapestPriceDate'] + ".")

    return game_list

#Commands

@client.command(pass_context=True, aliases = ['searchgames', 'SearchGames', 'SEARCHGAMES'])
async def search(ctx, title):
    author = ctx.message.author
    channel = ctx.message.channel
    print(ctx.message)
    print(title)
    data = get_games_by_name(title)
    print(data)
    game_list = await parse_games(channel, data)
    print(channel, game_list)
    

@client.command(pass_context=True, aliases = ['Help', 'HELP'])
async def help(ctx):
    help = "You have asked for help!\nThis discord bot is capable of requesting the best game deals from a Public API across multiple platforms.\nCommands:\n`!searchgames {game name}` - Sends results for the cheapest price now as well as the cheapest price ever for a given game title. Limited to the top 5 matches for game name."
    author = ctx.message.author
    channel = ctx.message.channel
    await channel.send(help) 


client.run(TOKEN, reconnect=True)