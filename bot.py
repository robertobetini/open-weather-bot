import discord

from keys import DISCORD_TOKEN
from commands import current, daily, hourly, minutely, units

client = discord.Client()

@client.event
async def on_connect():
  print("Connected to Discord.")

@client.event
async def on_disconnect():
  print("Disconnected from Discord.")

@client.event
async def on_ready():
  print("Open Weather Bot is ready.")

@client.event
async def on_message(message):
  if message.author != client.user:

    msg = message.content

    if client.user.id in message.raw_mentions:
      await message.channel.send("Available commands: !current, !minutely, !hourly, !daily, !units")

    elif msg.startswith("!current"):
      local = msg.replace("!current", "").strip()
      await current(message, local)

    elif msg.startswith("!daily"):
      local = msg.replace("!daily", "").strip()
      await daily(message, local)

    elif msg.startswith("!hourly"):
      local = msg.replace("!hourly", "").strip()
      await hourly(message, local)

    elif msg.startswith("!minutely"):
      local = msg.replace("!minutely", "").strip()
      await minutely(message, local)

    elif msg.startswith("!units"):
      arg = msg.replace("!units", "").strip()
      await units(message, arg)

client.run(DISCORD_TOKEN)