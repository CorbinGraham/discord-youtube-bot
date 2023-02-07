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

  video, source = search(query)
  voice = get(bot.voice_clients, guild=ctx.guild)

  await join(ctx, voice)
  await ctx.send(f'Now playing.')

  voice = get(bot.voice_clients, guild=ctx.guild)

  voice.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))
  voice.is_playing()

bot.run(TOKEN)