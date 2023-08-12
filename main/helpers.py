import pytz
from dotenv import load_dotenv
from datetime import datetime
import requests

import os
load_dotenv()
WEATHER_KEY = os.getenv("WEATHERAPI_KEY")

weather_fields = {
    "current": ["temp_c", "temp_f", "wind_mph", "wind_kph", "wind_dir", "precip_mm", "precip_in", "humidity", "condition"],
    "location": ["name", "country", "tz_id", "localtime"],
}

def evaluate(expr):
    try:
        return eval(expr)
    except:
        return None

def get_current_time_in_tz(tz):
    utc_now = datetime.utcnow()
    desired_tz = pytz.timezone(tz)
    local_time = utc_now.replace(tzinfo=pytz.utc).astimezone(desired_tz)
    return local_time.strftime("%H:%M:%S")

def get_current_weather(loc):
    # TODO: cache results + robust handling
    url = 'http://api.weatherapi.com/v1/current.json?key={k}&q={q}&aqi=no'.format(k=WEATHER_KEY, q=loc)
    res = requests.get(url).json()
    out = {'current': {}, 'location': {}}
    if res:
        for k in weather_fields.keys():
            for f in weather_fields[k]:
                out[k][f] = res[k].get(f)
    return out 
