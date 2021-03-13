# store and get tokens from environment
import os
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
LINK = os.getenv("LINK")

from discord.ext import commands
import playlistmaker
import requests

# create a bot that can take commands
bot = commands.Bot(command_prefix='!nm ')

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

@bot.command(brief='Checks if bot is online')
async def ping(ctx):
    await ctx.send(f"pong! ({round(bot.latency * 1000)}ms) ")

spotify_url_format = "https://open.spotify.com/track/"
spotify_url_format2 = "https://link.tospotify.com/"

# helper function to make sure messages aren't added twice
def not_yet_added(message):
    for reaction in message.reactions:
        if reaction.emoji == "✅":
            return False
    return True

@bot.command(brief='Adds all Spotify links in a channel to a playlist')
async def collect(ctx):
    await ctx.send("collecting...")
    
    channel = ctx.channel
    messages = await channel.history(limit=None).flatten()
    
    # position counter to add songs in order
    n = 0
    
    # iterate through all messages and add each track to playlist
    for message in messages:
        if spotify_url_format in message.content or spotify_url_format2 in message.content:
            if not_yet_added(message):

                # isolate the url portion:
                start_index = message.content.find("http")
                trackURL = message.content[start_index:]
                # slice off extra slashes (they seem to break the spotify link recognizer)
                if message.content.count("/") > 4:
                    end_index = message.content.rfind("/")
                    trackURL = message.content[:end_index]
                
                # check if it's a link.tospotify kind of link
                if spotify_url_format2 in trackURL: #skyeh
                    r = requests.get(trackURL)
                    trackURL = r.url

                # try adding the song to the playlist
                try:
                    playlistmaker.addTrack(trackURL, n)
                    await message.add_reaction("✅")
                    n = n + 1
                except: #catch all exceptions, skip track if error
                    await message.add_reaction("🟥")

            else: # reached an already added track, so skip
                await ctx.send("done!")
                return

@bot.command(brief='Removes all ✅ reactions in this channel (may lead to duplicate songs)')
async def uncheck(ctx):
    channel = ctx.channel
    messages = await channel.history(limit=None).flatten()
    for message in messages:
        await message.remove_reaction("✅", bot.user)
    await ctx.send("finished removing checks")

@bot.command(brief='Removes all red box reactions in this channel')
async def uncheckred(ctx):
    channel = ctx.channel
    messages = await channel.history(limit=None).flatten()
    for message in messages:
        await message.remove_reaction("🟥", bot.user)

@bot.command(brief="Sends link to playlist")
async def link(ctx):
    await ctx.send(LINK)

@bot.command(brief="Deletes all bot-related messages in channel (commands, responses)")
async def cleanup(ctx, limit=0, notice=True):
    if notice:
        await ctx.send("attempting to delete bot-related messages...")
    channel = ctx.channel
    messages = await channel.history(limit=None).flatten()
    if limit == 0:
        for message in messages:
            if message.content.startswith("!nm ") or message.author == bot.user:
                await message.delete()
    else:
        for message in messages:
            if limit == 0:
                return
            else:
                if message.content.startswith("!nm ") or message.author == bot.user:
                    limit = limit - 1
                    await message.delete()

bot.run(DISCORD_TOKEN)
