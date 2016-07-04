from datetime import datetime
import os
import requests
import json
import argparse

year = str(datetime.now().year)
month = str(datetime.now().month)
day = str(datetime.now().day)
apiKey = "14c4dc54-572f-4e6b-9b85-b0d9aa06be7d"
wakaApi = "https://wakatime.com/api/v1/users/current/summaries?api_key={api}&start={year}-{month}-{day}&end={year}-{month}-{day}".format(year=year, month=month, day=day, api=apiKey)

def summaries(path):
  try:
    r = requests.get(wakaApi)
    json_data = json.loads(r.content)
    horas = json_data["data"][0]["grand_total"]["hours"]
    minutos = json_data["data"][0]["grand_total"]["minutes"]
    time_text = json_data["data"][0]["grand_total"]["text"]

    file = '{base}/{day}.md'.format(base=path, day=day)

    log_file = u'# Codeando el {day}/{month}/{year}\n\n## Tiempo total\n{tiempo}.\n'.format(day=day, month=month, year=year, tiempo=time_text)

    if len(json_data["data"][0]["languages"]) > 0:
      log_file += '\n## Lenguajes usados\n'
      for l in json_data["data"][0]["languages"]:
        log_file += '1. {language} con {tiempo} ({porcentaje}%)\n'.format(language=l["name"], tiempo=l["text"], porcentaje=l["percent"])

    if len(json_data["data"][0]["projects"]) > 0:
      log_file += '\n## Proyectos actualizados\n'
      for p in json_data["data"][0]["projects"]:
        log_file += '1. {proyecto} con {tiempo} ({porcentaje}%)\n'.format(proyecto=p["name"], tiempo=p["text"], porcentaje=p["percent"])

    if len(json_data["data"][0]["operating_systems"]) > 0:
      log_file += '\n## Plataformas utilizadas\n'
      for s in json_data["data"][0]["operating_systems"]:
        log_file += '1. {sistema} con {tiempo} ({porcentaje}%)\n'.format(sistema=s["name"], tiempo=s["text"], porcentaje=s["percent"])

    sb = open(file, 'w')
    sb.write(log_file)
  except Exception, e:
    print "Error: ",e

parser = argparse.ArgumentParser(description='Se obtiene la informacion del sitio WakaTime.')
parser.add_argument('-p', '--path', action='store', default=False, help='Carpeta donde almacena el log del dia.')

args = parser.parse_args()

if not args.path:
  parser.print_help()
else:
  summaries(args.path)