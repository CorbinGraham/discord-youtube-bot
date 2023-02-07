# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import requests
import os
from youtube_dl import YoutubeDL
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
import asyncio

# The API token must be set as an environment variable.
TOKEN = ''

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)
video_queue = []

# TODO: Implement proper queue
# TODO: Implement skipping
# TODO: Implement search with options

def search(query):
  with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
    try: requests.get(query)
    except: info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
    else: info = ydl.extract_info(query, download=False)
  return (info, info['formats'][0]['url'])


async def join(ctx, voice):
  channel = ctx.author.voice.channel

  if voice and voice.is_connected():
    await voice.move_to(channel)
  else:
    voice = await channel.connect()
  return voice

@bot.command()
async def play(ctx, *, query):
  FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

  voice = get(bot.voice_clients, guild=ctx.guild)

  if voice and voice.is_connected() and ctx.voice_client.is_playing():
    video_queue.append(query)
    await ctx.send(f"Video queued as number #{len(video_queue)}")
    return

  await join(ctx, voice)
  await ctx.send(f'Now playing')

  voice = get(bot.voice_clients, guild=ctx.guild)
  video, source = search(query)

  voice.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda ctx: (await play(ctx, video_queue.pop) for _ in '_').__anext__())
  voice.is_playing()

@bot.command()
async def skip(ctx):
  voice = get(bot.voice_clients, guild=ctx.guild)
  if voice and voice.is_connected() and ctx.voice_client.is_playing():
    await voice.stop()
    if video_queue:
      play(ctx, video_queue.pop)
  else:
    await ctx.send(f"OwO I'm not playing anything")

bot.run(TOKEN)