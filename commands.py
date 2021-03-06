import requests
import io
import discord
import datetime
import os


from matplotlib import pyplot as plt
from setup import update_settings, save_settings, init_settings
from settings_validation import valid_units
from owapi import get_current_json, get_onecall_json
from emotes import ID_to_emote
from setup import TEMP_UNIT

async def units(message, unit):
  settings = init_settings()
  channel = message.channel

  if unit in valid_units:
    update_settings(settings, units=unit)
    save_settings(settings)
    await channel.send(f"Unit system changed to **{unit}**")
  else:
    await channel.send("Availabe unit systems: standard, metric, imperial (ex: !units metric)")


async def current(message, local):
  settings = init_settings()
  channel = message.channel
  mention = message.author.mention

  if local:
    data = get_current_json(local, settings)
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
  {description.capitalize()} {emotes} at **{local} ({country})** (*lat = {lat}, lon = {lon}*)
```
Temperature - {temperature}{TEMP_UNIT[settings["units"]]}
Feels like - {feels_like}{TEMP_UNIT[settings["units"]]}
Min and max temperatures - {temp_min} ~ {temp_max}{TEMP_UNIT[settings["units"]]}
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
      await channel.send(f"{mention} local -> **{local}** <- not found")
  else:
    await channel.send("!current <location> (ex: !current moscow)")


async def daily(message, local):
  settings = init_settings()
  channel = message.channel
  mention = message.author.mention

  if local:
    data = get_onecall_json(local, "daily", settings)

    name_and_country = get_current_json(local)
    city = name_and_country['name']
    country = name_and_country['sys']['country']

    reply = f"Forecast for the next 7 days at **{city} ({country})**:\n\n"

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
        line += f"\t:sunny:\t{temp_day}{TEMP_UNIT[settings['units']]}\n"
        line += f"\t:crescent_moon:\t{temp_night}{TEMP_UNIT[settings['units']]}\n\n"
        reply += line

      await channel.send(reply[:-2])
    else:
      await channel.send(f"{mention} local -> **{local}** <- not found")
  else:
    await channel.send("!daily <location> (ex: !daily el salvador)")


async def hourly(message, local):
  settings = init_settings()
  channel = message.channel
  mention = message.author.mention

  try:
    os.mkdir("./img")
  except:
    pass

  if local:
    data = get_onecall_json(local, "hourly", settings)
        
    name_and_country = get_current_json(local)
    city = name_and_country['name']
    country = name_and_country['sys']['country']

    if data['cod'] == 200:
      hours = []
      temperatures = []
      humidity = []

      tdelta = datetime.timedelta(seconds=data['timezone_offset'])
      for hour in data['hourly']:
        date = datetime.datetime.utcfromtimestamp(hour['dt'])
        date += tdelta
        day = date.date()
        date_hour = date.hour
        minutes = date.minute
        hours.append(f"{day} {date_hour}:{str(minutes).zfill(2)}")
        temperatures.append(hour['temp'])
        humidity.append(hour['humidity'])

      fig, axs = plt.subplots(2, sharex=True)
      fig.suptitle(f"Humidity and temperature at {city} ({country})")
      axs[0].plot(hours, temperatures, color="red")
      # axs[0].set_ylim(bottom=0)
      axs[0].set_autoscaley_on(True)
      axs[1].plot(hours, humidity, color="blue")
      axs[1].set_ylim(bottom=0, top=100)
      plt.xticks([0, len(hours) - 1], [hours[0], hours[-1]])

      axs.flat[0].set(ylabel=f"Temperature ({TEMP_UNIT[settings['units']]})")
      axs.flat[1].set(xlabel="Local time", ylabel="Humidity (%)")

      save_path = "./img/hours_graph.png"
      plt.savefig(save_path, dpi=128)
      plt.clf()

      img = open(save_path, "rb")
      await channel.send(f"Hourly forecast for the next 2 days at **{city} ({country})**:", file=discord.File(img, 'graph.png'))
      img.close()
      os.remove(save_path)

    else:
      await channel.send(f"{mention} local -> **{local}** <- not found")
  else:
    await channel.send("!hourly <location> (ex: !hourly london)")


async def minutely(message, local):
  settings = init_settings()
  channel = message.channel
  mention = message.author.mention

  try:
    os.mkdir("./img")
  except:
    pass
      
  if local:
    data = get_onecall_json(local, "minutely", settings)
        
    name_and_country = get_current_json(local)
    city = name_and_country['name']
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
      plt.title(f"Precipitation at {city} ({country})")
      plt.ylim(bottom=0)
      plt.xlabel("Local time")
      plt.ylabel("Precipitation (mm)")
      plt.xticks([0, len(minutes) - 1], [minutes[0], minutes[-1]])

      save_path = "./img/minutes_graph.png"
      plt.savefig(save_path, dpi=128)
      plt.clf()

      img = open(save_path, "rb")
      await channel.send(f"Precipitation forecast for the nex 60 minutes at **{city} ({country})**:", file=discord.File(img, 'graph.png'))
      img.close()
      os.remove(save_path)
    else:
      await channel.send(f"{mention} local -> **{local}** <- not found")
  else:
    await channel.send("!minutely <location> (ex: !minutely rio de janeiro)")