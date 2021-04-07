# -*- coding: utf-8 -*-
from datetime import datetime
import os
import requests
import json
import argparse

year = str(datetime.now().year)
month = datetime.now().strftime('%m')
day = datetime.now().strftime('%d')
urlBase = "https://wakatime.com/api/v1/users/current/summaries?api_key={token}&start={year}-{month}-{day}&end={year}-{month}-{day}"
access_token = ''

def getToken():
    token = access_token
    if token == '':
        f = open('../access.json', 'r')
        data = json.loads(f.read())
        if 'wakaTime' in data:
            token = data['wakaTime']
    return token

def summaries(path):
    try:
        wakaApi = urlBase.format(token=access_token,year=year, month=month, day=day)
        r = requests.get(wakaApi)
        json_data = json.loads(r.content)
        horas = json_data["data"][0]["grand_total"]["hours"]
        minutos = json_data["data"][0]["grand_total"]["minutes"]
        time_text = json_data["data"][0]["grand_total"]["text"]

        file = '{base}/{day}.md'.format(base=path, day=day)

        log_file = u'# Codeando el {day}/{month}/{year}\n\n## Tiempo total\n{tiempo}.\n'.format(day=day, month=month, year=year, tiempo=time_text)

        if len(json_data["data"][0]["languages"]) > 0:
            log_file += u'\n## Lenguajes usados\n'
            for l in json_data["data"][0]["languages"]:
                log_file += u'1. {language} con {tiempo} ({porcentaje}%)\n'.format(language=l["name"], tiempo=l["text"], porcentaje=l["percent"]).encode('ascii', 'ignore').decode('ascii')

        # if len(json_data["data"][0]["projects"]) > 0:
        #   log_file += u'\n## Proyectos actualizados\n'
        #   for p in json_data["data"][0]["projects"]:
        #     log_file += u'1. {proyecto} con {tiempo} ({porcentaje}%)\n'.format(proyecto=p["name"], tiempo=p["text"], porcentaje=p["percent"]).encode('ascii', 'ignore').decode('ascii')

        if len(json_data["data"][0]["operating_systems"]) > 0:
            log_file += u'\n## Plataformas utilizadas\n'
            for s in json_data["data"][0]["operating_systems"]:
                log_file += u'1. {sistema} con {tiempo} ({porcentaje}%)\n'.format(sistema=s["name"], tiempo=s["text"], porcentaje=s["percent"]).encode('ascii', 'ignore').decode('ascii')

        if len(json_data["data"][0]["editors"]) > 0:
            log_file += u'\n## IDEs\n'
            for e in json_data["data"][0]["editors"]:
                log_file += u'1. {editor} un total de {tiempo} ({porciento}%)\n'.format(editor=e["name"], tiempo=e["digital"], porciento=e["percent"]).encode('ascii', 'ignore').decode('ascii')

        sb = open(file, 'w')
        sb.write(log_file)
    except Exception as e:
        print("Error: ",e)

parser = argparse.ArgumentParser(description='Se obtiene la informacion del sitio WakaTime.')
parser.add_argument('-p', '--path', action='store', default=False, help='Carpeta donde almacena el log del dia.')

args = parser.parse_args()
access_token = getToken()

if not args.path:
    parser.print_help()
else:
    summaries(args.path)
