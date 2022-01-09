# store and get tokens from environment
import os
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
LINK = os.getenv("LINK")

from discord.ext import commands
import playlistmaker
import requests
import heapq

description = 'nice music bot collects all your spotify links into a playlist! \n \n just run "!nm collect" in the channel you want to collect songs from, and theyll show up in the playlist found at "!nm link". \n \n while collecting, the bot will react with a ✅ to the songs it has successfully added.  In the event of errors, you can retry adding those songs by running "!nm uncheckred" and then "!nm collect" again.'

help_command = commands.DefaultHelpCommand(
    no_category = 'List of commands'
)

# create a bot that can take commands
bot = commands.Bot(
    command_prefix='!nm ',
    description = description,
    help_command = help_command
)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

@bot.command(brief='Check if bot is online')
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

@bot.command(brief='Add all Spotify links in a channel to a playlist')
async def collect(ctx):
    waiting_message = await ctx.send("collecting...")
    
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
                    playlistmaker.add_track(trackURL, n)
                    await message.add_reaction("✅")
                    n = n + 1

                    # # update contributions for leaderboard 
                    # if contributions: # but don't update if there is no history
                    #     if message.user.display_name in contributions:
                    #         contributions[message.user.display_name] += 1
                    #     else:
                    #         contributions[message.user.display_name] = 1

                except: #catch all exceptions, skip track if error
                    await message.add_reaction("🟥")

            else: # reached an already added track, so skip
                await waiting_message.delete()
                await ctx.send("done!", delete_after=60.0)
                return

@bot.command(brief='Removes all ✅ reactions in channel',
    help = 'Removes all ✅ reactions in channel. If you run "!nm collect" again, this lets you re-add all the songs. However, this may lead to duplicate songs! '
)
async def uncheck(ctx):
    channel = ctx.channel
    messages = await channel.history(limit=None).flatten()
    for message in messages:
        await message.remove_reaction("✅", bot.user)
    await ctx.send("finished removing checks")

@bot.command(brief='Remove all red box reactions in this channel')
async def uncheckred(ctx):
    channel = ctx.channel
    messages = await channel.history(limit=None).flatten()
    for message in messages:
        await message.remove_reaction("🟥", bot.user)

@bot.command(brief="Send a link to the playlist")
async def link(ctx):
    await ctx.send(LINK)

@bot.command(brief="Delete all bot-related messages in channel",
    help = "Deletes any !nm commands sent by users & messages sent by the bot in the specified channel. You can also specify a limit to the number of messages to delete, for instance, !nm cleanup 3 will delete the last 3 messages."
)
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


@bot.command(brief='Remove duplicate tracks from the playlist',
    help = "Finds songs that have been added to the playlist more than once and removes the duplicates from the playlist. This action cannot be undone."
)
async def dedup(ctx):
    await ctx.send("removing duplicates...")
    dups, num = playlistmaker.find_duplicate_tracks(playlistmaker.get_playlist_tracks())
    if num == 0:
        await ctx.send("no duplicates were found" )
        return
    items = playlistmaker.itemize_duplicates(dups)
    playlistmaker.remove_duplicates(items)
    await ctx.send("found and removed " + str(num) + " duplicates!" )

def count_contributions(messages):
    contributions = {}
    for message in messages:
        if spotify_url_format in message.content or spotify_url_format2 in message.content:
            if message.author.display_name in contributions:
                contributions[message.author.display_name] += 1
            else:
                contributions[message.author.display_name] = 1
    return contributions


def build_leaderboard(messages):
    contributions = count_contributions(messages)
    leader_heap = []
    for user in contributions:
        heapq.heappush(leader_heap, [-(contributions[user]), user])
        print(leader_heap)
    return leader_heap


@bot.command(brief='See who shared the most songs in this channel!')
async def leaderboard(ctx, topk=10):
    waiting_message = await ctx.send("calculating leaderboard...")
    channel = ctx.channel
    messages = await channel.history(limit=None).flatten()
    heap = build_leaderboard(messages)
    top_list = []
    print(heap)
    for i in range(1, topk + 1):
        if heap == []:
            break
        num, user = heapq.heappop(heap)
        top_list.append(str(i) + ". " + user + ", with " + str(-num) + " songs")
    await waiting_message.delete() 
    await ctx.send("top " + str(i - 1) + " contributors:\n```" + "\n".join(top_list) + "```")


bot.run(DISCORD_TOKEN)
