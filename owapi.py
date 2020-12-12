import requests

WEATHER_API_KEY = "301b49bb262eddccc54eb7908961ad2b"
onecall_options = ["minutely", "hourly", "daily", "current", "alerts"]

# url = api + query_string
weather_api = "https://api.openweathermap.org/data/2.5"
weather_onecall = weather_api + "/onecall?"
weather_current = weather_api + "/weather?"


def get_current_json(city, settings={"units": "metric"}):
  query_string = f"q={city}&appid={WEATHER_API_KEY}&units={settings['units']}&lang=en"
  url = weather_current + query_string
  req = requests.get(url)
  return req.json()

def get_onecall_json(city, option, settings={"units": "metric"}):
  '''
  Option can be "minutely", "hourly", "daily", "current", "alerts".
  '''
  # preparing for onecall
  city_info = get_current_json(city)
  if city_info['cod'] != 200:
    return city_info
  lat = city_info['coord']['lat']
  lon = city_info['coord']['lon']

  exclude = ""
  for opt in onecall_options:
    if opt == option:
      continue
    exclude += opt + ","

  # making a onecall call
  query_string = f"lat={lat}&lon={lon}&exclude={exclude[:-1]}&appid={WEATHER_API_KEY}&units={settings['units']}&lang=en"
  url = weather_onecall + query_string
  req = requests.get(url)
  data = req.json()
  data['cod'] = 200
  return data