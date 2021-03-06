PATH = "./config.txt"

TEMP_UNIT = {
  "metric": "°C",
  "imperial": "°F",
  "standard": "K"
}

def init_settings():
  first_time_running = True 

  try:
    open(PATH, "x")
  except:
    first_time_running = False

  settings = {}
  if first_time_running:
    cfg_file = open(PATH, "a")
    cfg_file.write("units=metric")
    cfg_file.close()
  
  with open(PATH, "r") as file:
    for line in file:
      attributes = line.split("=")
      if line[-1] == "\n":
        settings[attributes[0]] = attributes[1][:-1]
      else:
        settings[attributes[0]] = attributes[1]

  return settings

def save_settings(settings):
  cfg_file = open(PATH, "w")
  cfg_file.write(f"units={settings['units']}")
  cfg_file.close()

def update_settings(settings, units=None):
  if units:
    settings["units"] = units