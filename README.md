# Cheap Bot
A [Cheapshark](www.cheapshark.com) API powered discord bot

## Prerequisites

This bot was written with Python Version 3.9.2. 

To install prerequisites run `pip install -r requirements.txt` in the `src` directory.

## Commands

`!deals *input*` - Search for the top 5 games matching the game name `input` and returns the results.

## How to setup your own bot hosting
1. [Create your Discord bot account](https://discordpy.readthedocs.io/en/latest/discord.html)  
    1a. The required scopes for this bot are currently ```bot```.
2. Clone/download this repository  
3. Open the `src` directory.  
4. Rename [config.example.txt](config.example.txt) to `config.txt` then insert your own discord API bot token.
5. In the `src` directory run `py app.py`

## How to run Cheap-Bot via Docker

1. [Create your Discord bot account](https://discordpy.readthedocs.io/en/latest/discord.html)  
    1a. The required scopes for this bot are currently ```bot```.
2. Clone/download this repository  
3. Open the `src` directory.  
4. In the `src` directory run `docker build -t cheapbot .`
5. In the `src` directory run `docker run -it -e BOTTOKEN="INSERT YOUR TOKEN HERE" -p 80:80 cheapbot`

## Additional Documentation
- [Cheapshark API documentation](https://apidocs.cheapshark.com/#intro)
