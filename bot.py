import discord
import io
import requests
import datetime
import os

from matplotlib import pyplot as plt
from owapi import get_current_json, get_onecall_json
from emotes import ID_to_emote
from setup import init_settings, update_settings, save_settings
from settings_validation import valid_units

# Todo:
#
# 1. Make the bot create a config.txt file to store user preferences
# 2. Make the bot read the file and set the preferences

settings = init_settings()

client = discord.Client()

DISCORD_TOKEN = "Nzg2MDM1ODAwMjk0MjkzNTI2.X9Ai4g.X2UjjxEraf0HQE-1F5XMNwkcnBw"

@client.event
async def on_ready():
  print("Open Weather Bot is ready.")

@client.event
async def on_message(message):
  if message.author != client.user:

    #################################
    msg = message.content.split(" ")
    channel = message.channel
    # author = message.author
    mention = message.author.mention
    #################################

    # concatenating the argument strings
    arg = ""
    for i in range(len(msg)):
      if i != 0:
        arg += msg[i] + " "
    arg = arg.strip()


    if msg[0] == "!current" and arg:
      data = get_current_json(arg, settings)
      if data['cod'] == 200:
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        local = data['name']
        country = data['sys']['country']
        description = data['weather'][0]['description']
        emotes = ID_to_emote[data['weather'][0]['id']]
        temperature = round(float(data['main']['temp']), 1)
        feels_like = round(float(data['main']['feels_like']), 1)
        temp_min = round(float(data['main']['temp_min']), 1)
        temp_max = round(float(data['main']['temp_max']), 1)
        humidity = data['main']['humidity']
        nebulosity = data['clouds']['all']
        try:
          pressure = round(data['main']['grnd_level']/1000, 3)
        except:
          pressure = round(data['main']['pressure']/1000, 3)

        weather_string = f'''
{description.capitalize()} {emotes} at **{local} ({country})** (*latitude = {lat}, longitude = {lon}*)

```
Temperature - {temperature}°C
Feels like - {feels_like}°C
Min and max temperatures - {temp_min} ~ {temp_max}°C
Pressure - {pressure} bar
Humidity - {humidity}%
Nebulosity - {nebulosity}%
```
        '''
        icon_name = data['weather'][0]['icon']
        icon_url = "http://openweathermap.org/img/wn/"
        icon = requests.get(f"{icon_url}{icon_name}@4x.png").content # bytes
        icon = discord.File(io.BytesIO(icon), filename="icon.png")
        await channel.send(weather_string, file=icon)
      else:
        await channel.send(f"{mention} local -> **{arg}** <- not found")


    if msg[0] == "!daily" and arg:
      data = get_onecall_json(arg, "daily", settings)

      name_and_country = get_current_json(arg)
      local = name_and_country['name']
      country = name_and_country['sys']['country']

      reply = f"Forecast for the next 7 days at **{local} ({country})**:\n\n"

      if data['cod'] == 200:
        for day in data['daily'][1:]:
          temp_day = round(float(day['temp']['day']), 1)
          temp_night = round(float(day['temp']['night']), 1)
          description = day['weather'][0]['description']
          emotes = ID_to_emote[day['weather'][0]['id']]
          date = datetime.datetime.fromtimestamp(day['dt'])

          weekday_num_to_string = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
          week_day = weekday_num_to_string[date.weekday()]

          line = f"**{date.month}/{date.day} ({week_day}):** {description.capitalize()} {emotes}\n"
          line += f"\t:sunny:\t{temp_day}°C\n"
          line += f"\t:crescent_moon:\t{temp_night}°C\n\n"
          reply += line

        await channel.send(reply[:-2])
      else:
        await channel.send(f"{mention} local -> **{arg}** <- not found")


    if msg[0] == "!minutely" and arg:
      try:
        os.mkdir("./img")
      except:
        pass

      data = get_onecall_json(arg, "minutely", settings)
      
      name_and_country = get_current_json(arg)
      local = name_and_country['name']
      country = name_and_country['sys']['country']

      if data['cod'] == 200:
        minutes = []
        precipitation = []
        tdelta = datetime.timedelta(seconds=data['timezone_offset'])
        for minute in data['minutely']:
          date = datetime.datetime.utcfromtimestamp(minute['dt'])
          date += tdelta
          hour = date.hour
          date_minutes = date.minute
          minutes.append(f"{hour}:{str(date_minutes).zfill(2)}")
          precipitation.append(minute['precipitation'])

        plt.plot(minutes, precipitation, color="blue", linewidth=3)
        plt.title(f"Precipitation at {local} ({country})")
        plt.ylim(bottom=0)
        plt.xlabel("Local time")
        plt.ylabel("Precipitation (mm)")
        plt.xticks([0, len(minutes) - 1], [minutes[0], minutes[-1]])

        save_path = "./img/minutes_graph.png"
        plt.savefig(save_path, dpi=128)
        plt.clf()

        img = open(save_path, "rb")
        await channel.send(f"Precipitation forecast for the nex 60 minutes at **{local} ({country})**:", file=discord.File(img, 'graph.png'))
        img.close()
        os.remove(save_path)


    if msg[0] == "!units" and arg:
      if arg in valid_units:
        update_settings(settings, units=arg)
        save_settings(settings)
        await channel.send(f"Unit system changed to **{arg}**")
      elif arg == "help":
        await channel.send("Availabe unit systems: standard, metric, imperial")
      else:
        await channel.send("Choose a valid unit system (!units help)")

client.run(DISCORD_TOKEN)