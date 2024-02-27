# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import requests
import os
import yt_dlp
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
import asyncio

# The API token must be set as an environment variable.
TOKEN = os.environ.get('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)
video_queue = []

# TODO: Implement search with options

# Use youtube DL to download the youtube video for playing.
def search(query):
  with yt_dlp.YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
    try: requests.get(query)
    except: info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
    else: info = ydl.extract_info(query, download=False)
  return (info, info['formats'][0]['url'])

# This method is used for handeling playing songs that are in the queue.
# This is done outside of the "play" method since that would force the lambda
#   to run an async method.
def play_next(ctx):
  if video_queue:
    video, source = search(video_queue.pop(0))
    play_song(ctx, source)
  else:
    asyncio.run_coroutine_threadsafe(ctx.send("No more songs in queue."), bot.loop)

# Join the audio channel that the requesting user is connected to.
# If the bot is already in a channel, change to the channel of the most recent request.
async def join(ctx, voice):
  channel = ctx.author.voice.channel

  if voice and voice.is_connected():
    await voice.move_to(channel)
  else:
    voice = await channel.connect()
  return voice

# Start playing a queued song!
# If a song is already playing place it into a queue to be played next.
@bot.command()
async def play(ctx, *, query):
  voice = get(bot.voice_clients, guild=ctx.guild)

  if voice and voice.is_connected() and ctx.voice_client.is_playing():
    video_queue.append(query)
    await ctx.send(f"Video queued as number #{len(video_queue)}")
    print(f"queued a song. URL is : {query}")
    return

  await join(ctx, voice)
  await ctx.send(f'Now playing')

  voice = get(bot.voice_clients, guild=ctx.guild)
  video, source = search(query)

  play_song(ctx, source)
  voice.is_playing()

# Allows user to skip the current song.
# Simply does this by stopping the current running audio.
# If there is another song in the queue, the "play" or "play_next" method handles
# this automatically.
@bot.command()
async def skip(ctx):
  voice = get(bot.voice_clients, guild=ctx.guild)
  if voice and voice.is_connected() and ctx.voice_client.is_playing():
    voice.stop()
  else:
    await ctx.send(f"OwO I'm not playing anything")



################# MISC ###################
def play_song(ctx, source):
  FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  voice = get(bot.voice_clients, guild=ctx.guild)
  voice.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: play_next(ctx))

bot.run(TOKEN)
