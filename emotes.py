# discord emojis
clear_sky = ":sunny: "
few_clouds = ":white_sun_small_cloud: "
scattered_clouds = ":partly_sunny: "
broken_clouds = ":white_sun_cloud: "
overcast_clouds = ":cloud: "
rain = ":white_sun_rain_cloud: "
shower_rain = ":cloud_rain: "
thunderstorm = ":cloud_lightning: "
thunderstorm_rain = ":thunder_cloud_rain: "
snow = ":snowflake: "
mist = ":fog: "
warning = ":warning: "
green = ":green_circle: " # light
yellow = ":yellow_circle: " # moderate
red = ":red_circle: " # heavy

ID_to_emote = {
  200: thunderstorm_rain + green,
  201: thunderstorm_rain + yellow,
  202: thunderstorm_rain + red + warning,
  210: thunderstorm + green,
  211: thunderstorm + yellow,
  212: thunderstorm + red + warning,
  221: thunderstorm + green,
  230: thunderstorm_rain + green,
  231: thunderstorm_rain + yellow,
  232: thunderstorm_rain + red,

  300: shower_rain + green,
  301: shower_rain + yellow,
  302: shower_rain + red,
  310: shower_rain + green,
  311: shower_rain + yellow,
  312: shower_rain + red,
  313: shower_rain + green,
  314: shower_rain + red,
  321: shower_rain + yellow,

  500: rain + green,
  501: rain + yellow,
  502: rain + red,
  503: rain + red + warning,
  504: rain + red + warning,
  511: rain + snow + yellow,
  520: rain + green,
  521: rain + yellow + warning,
  522: rain + red + warning,
  531: rain + yellow,

  600: snow + green,
  601: snow + yellow,
  602: snow + red + warning,
  611: snow + rain + green,
  612: snow + shower_rain + green,
  613: snow + shower_rain + yellow + warning,
  615: snow + rain + green,
  616: snow + rain + yellow,
  620: snow + shower_rain + green,
  621: snow + shower_rain + yellow + warning,
  622: snow + shower_rain + red + warning,

  701: mist,
  711: mist,
  721: mist,
  731: mist,
  741: mist,
  751: mist,
  761: mist,
  762: mist + warning,
  771: mist + warning,
  781: mist + warning,

  800: clear_sky,

  801: few_clouds,
  802: scattered_clouds,
  803: broken_clouds,
  804: overcast_clouds
}