from datetime import datetime
import os
import requests
import json
import argparse

year = str(datetime.now().year)
month = datetime.now().strftime('%m')
day = datetime.now().strftime('%d')
units = "metric"
lang = "es"
ciudad = "Celaya,mx"
urlBase = "http://api.openweathermap.org/data/2.5/weather?q={ciudad}&units={units}&lang={lang}&APPID={api}"
access_token = ""

def getToken():
    token = access_token
    if token == '':
        f = open('../access.json', 'r')
        data = json.loads(f.read())
        if 'openWeather' in data:
            token = data['openWeather']
    return token

def current(path):
    try:
        urlApi = urlBase.format(ciudad=ciudad, units=units, lang=lang, api=access_token)
        r = requests.get(urlApi)
        json_data = json.loads(r.content)
        weather = json_data["weather"][0]["main"]
        weather_description = json_data["weather"][0]["description"]
        weather_icon = json_data["weather"][0]["icon"]
        temp = json_data["main"]["temp"]
        humedad = json_data["main"]["humidity"]
        wind = json_data["wind"]["speed"]
        clound = json_data["clouds"]["all"]

        file = '{base}/{day}.md'.format(base=path, day=day)

        log_file = u'# Clima en {ciudad} en el dia {day}\n\n'.format(ciudad=ciudad, day=day)

        if not os.path.isfile(file):
            sb = open(file, 'w')
            sb.write(log_file)
        else:
            sb = open(file, 'a')

        sb.write('1. A las {hour}:{minute} !["icon weather"](http://openweathermap.org/img/w/{icon}.png) tenemos una temperatura de {temp} C con {desc} y  vientos de {wind} y nubosidad al {clound}%\n'.format(
                hour=str(datetime.now().hour),
                minute=str(datetime.now().minute),
                icon=weather_icon,
                temp=temp,
                desc=weather_description,
                wind=wind,
                clound=clound
            ))
        sb.close()
    except Exception as e:
        print("Error: ",e)

parser = argparse.ArgumentParser(description='Obtenemos el estado actual de una ciudad (celaya) .')
parser.add_argument('-p', '--path', action='store', default=False, help='Carpeta donde almacena el log del dia')

args = parser.parse_args()
access_token = getToken()
if not args.path:
    parser.print_help()
else:
    current(args.path)
