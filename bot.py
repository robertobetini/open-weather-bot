import discord
import requests
import json
import io

client = discord.Client()

WEATHER_API_KEY = "301b49bb262eddccc54eb7908961ad2b"
DISCORD_TOKEN = "Nzg2MDM1ODAwMjk0MjkzNTI2.X9Ai4g.X2UjjxEraf0HQE-1F5XMNwkcnBw"

# url = api + query_string
weather_api = "https://api.openweathermap.org/data/2.5"
weather_onecall = weather_api + "/onecall?"
weather_daily = weather_api + "/forecast/daily?"
weather_current = weather_api + "/weather?"

@client.event
async def on_ready():
  print("Open Weather Bot is ready.")

@client.event
async def on_message(message):
  if message.author != client.user:

    #################################
    msg = message.content.split(" ")
    channel = message.channel
    author = message.author
    mention = message.author.mention
    #################################

    arg = ""
    for i in range(len(msg)):
      if i != 0:
        arg += msg[i] + " "
    arg = arg.strip()
    if msg[0] == "!current":
      query_string = f"q={arg}&appid={WEATHER_API_KEY}&units=metric&lang=pt_br"
      url = weather_current + query_string
      req = requests.get(url)

      # all weather data are here in response
      data = req.json()
      if data['cod'] == 200:
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        local = data['name']
        pais = data['sys']['country']
        tempo = data['weather'][0]['description']
        temperatura = round(float(data['main']['temp']), 1)
        sensacao = round(float(data['main']['feels_like']), 1)
        temp_min = round(float(data['main']['temp_min']), 1)
        temp_max = round(float(data['main']['temp_max']), 1)
        umidade = data['main']['humidity']
        nebulosidade = data['clouds']['all']
        try:
          pressao = round(data['main']['grnd_level']/1000, 3)
        except:
          pressao = round(data['main']['pressure']/1000, 3)

        weather_string = f'''
Tempo em **{local} ({pais})** (*latitude = {lat}, longitude = {lon}*)

```
Tempo - {tempo}
Temperatura - {temperatura}°C
Sensação térmica - {sensacao}°C
Temperaturas mínima e máxima - {temp_min} ~ {temp_max}°C
Pressão atmosférica - {pressao} bar
Umidade relativa do ar - {umidade}%
Nebulosidade - {nebulosidade}%
```
        '''
        icon_name = data['weather'][0]['icon']
        icon_url = "http://openweathermap.org/img/wn/"
        icon = requests.get(f"{icon_url}{icon_name}@4x.png").content # bytes
        icon = discord.File(io.BytesIO(icon), filename="img.png")
        await channel.send(weather_string, file=icon)
      else:
        await channel.send(f"{mention} local -> **{arg}** <- não encontrado")

client.run(DISCORD_TOKEN)