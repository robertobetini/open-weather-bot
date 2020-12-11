import discord
import requests
import io
import datetime
import os

from matplotlib import pyplot as plt
from owapi import get_current_json, get_onecall_json
from emotes import ID_to_emote

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
      data = get_current_json(arg)
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
{description.capitalize()} {emotes} em **{local} ({country})** (*latitude = {lat}, longitude = {lon}*)

```
Temperatura - {temperature}°C
Sensação térmica - {feels_like}°C
Temperaturas mínima e máxima - {temp_min} ~ {temp_max}°C
Pressão atmosférica - {pressure} bar
Umidade relativa do ar - {humidity}%
Nebulosidade - {nebulosity}%
```
        '''
        icon_name = data['weather'][0]['icon']
        icon_url = "http://openweathermap.org/img/wn/"
        icon = requests.get(f"{icon_url}{icon_name}@4x.png").content # bytes
        icon = discord.File(io.BytesIO(icon), filename="icon.png")
        await channel.send(weather_string, file=icon)
      else:
        await channel.send(f"{mention} local -> **{arg}** <- não encontrado")

    if msg[0] == "!daily" and arg:
      data = get_onecall_json(arg, "daily")

      name_and_country = get_current_json(arg)
      local = name_and_country['name']
      country = name_and_country['sys']['country']

      reply = f"Previsão para os próximos 7 dias em **{local} ({country})**:\n\n"

      if data['cod'] == 200:
        for day in data['daily'][1:]:
          temp_day = round(float(day['temp']['day']), 1)
          temp_night = round(float(day['temp']['night']), 1)
          description = day['weather'][0]['description']
          emotes = ID_to_emote[day['weather'][0]['id']]
          date = datetime.datetime.fromtimestamp(day['dt'])

          weekday_num_to_string = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
          week_day = weekday_num_to_string[date.weekday()]

          line = f"**{date.day}/{date.month} ({week_day}):** {description.capitalize()} {emotes}\n"
          line += f"\t:sunny:\t{temp_day}°C\n"
          line += f"\t:crescent_moon:\t{temp_night}°C\n\n"
          reply += line

        await channel.send(reply[:-2])
      else:
        await channel.send(f"{mention} local -> **{arg}** <- não encontrado")

    if msg[0] == "!minutely":
      data = get_onecall_json(arg, "minutely")
      
      name_and_country = get_current_json(arg)
      local = name_and_country['name']
      country = name_and_country['sys']['country']

      minutos = []
      precipitacao = []      

      for minute in data['minutely']:
        date = datetime.datetime.fromtimestamp(minute['dt'])
        hour = date.hour
        minutes = date.minute
        minutos.append(f"{hour}:{minutes}")
        precipitacao.append(minute['precipitation'])

      plt.plot(minutos, precipitacao, color="blue", linewidth=3)
      plt.title(f"Precipitação em {local} ({country})")
      plt.ylim(bottom=0)
      plt.xlabel("Tempo")
      plt.ylabel("Precipitação (mm)")
      plt.xticks([0, len(minutos)], [minutos[0], minutos[-1]])

      save_path = "./img/minutes_graph.png"
      plt.savefig(save_path, dpi=128)

      try:
        os.mkdir("./img")

      img = open(save_path, "rb")
      await channel.send(f"Previsão de precipitação para os próximos 60 minutos em **{local} ({country})**:", file=discord.File(img, 'graph.png'))
      img.close()
      os.remove(save_path)

client.run(DISCORD_TOKEN)