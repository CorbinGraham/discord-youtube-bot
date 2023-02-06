# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import os
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio

# The API token must be set as an environment variable.
TOKEN = str(os.environ['002TOKEN'])

client = discord.Client()

bot = commands.Bot(command_prefix="/")

@client.event
async def on_message(message):

  # we do not want the bot to reply to itself
  if message.author == client.user:
    return

  if message.content.startswith('/play'):
    msg = youtube_player.enqueue_play(message.content.split(" ")[1])
    connected_users = enqueue_episode.find_users(message)
    await client.send_message(message.channel, msg)

  if message.content.startswith('/skip'):
    msg = youtube_player.play(message, message.content.split(" "))
    connected_users = enqueue_episode.find_users(message)
    await client.send_message(message.channel, msg)

    await client.send_message(message.channel, msg)
    if msg == 'BAKA! I need something to enqueue!':
      return


@client.event
async def on_voice_state_update(before, after):
  if watched_channel != None:
    if (before.voice_channel != watched_channel) and (after.voice_channel == watched_channel):
      await client.send_message(tts_announce_channel, after.name + ' has joined channel', tts = True)

    elif (before.voice_channel == watched_channel) and (after.voice_channel != watched_channel):
      await client.send_message(tts_announce_channel, after.name + ' has left channel', tts = True)

@bot.command(pass_context=True)
async def join(ctx):
  author = ctx.message.author
  channel = author.voice_channel
  await bot.join_voice_channel(channel)

@client.event
async def on_ready():
  print('Logged in as')
  print(client.user.name)
  print(client.user.id)
  print('------')

client.run(TOKEN)