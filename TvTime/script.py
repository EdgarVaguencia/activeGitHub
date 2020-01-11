import os
import requests
import json
import argparse

access_token = ''
urlBase = 'https://api.tvtime.com/v1/{method}?access_token={token}'
path = ''

def formatName(name):
    nameFormat = name
    character = ['*', ':', '?', '/', '<', '>', '|']
    for c in character:
        nameFormat = nameFormat.replace(c, '')
    return nameFormat


def getShows(show_id, page=0):
    if show_id == 'All':
        urlApi = urlBase.format(method='library', token=access_token) + '&limit=200&page={pag}'.format(pag=page)
        try:
            r = requests.get(urlApi)
            json_data = json.loads(r.content)
            shows = json_data['shows']
            if len(shows) > 0:
                dir_path = '{path}/{folder}'.format(path=path, folder='series')
                if not os.path.isdir(dir_path):
                    os.mkdir(dir_path)
                for s in shows:
                    showName = formatName(s['name'])
                    file = u'{dir}/{name}.md'.format(dir=dir_path, name=showName)

                    log_file = '# {name} ({number})\n\n'.format(name=showName, number=s['id'])
                    log_file += '<img src="{}" />\n\n'.format(s['all_images']['poster']['0'])
                    log_file += '## Status\n* {}\n'.format(s['status'])
                    log_file += '## Last Aired\n* Season: {sesson}\n* Episode: {episode}\n'.format(sesson=s['last_aired']['season_number'], episode=s['last_aired']['number'])

                    if s['last_seen']:
                        log_file += '## Last Seen\n* Season: {sesson}\n* Episode: {episode}\n'.format(sesson=s['last_seen']['season_number'], episode=s['last_seen']['number'])
                    log_file += '## Seen Episodes\n* Total: {total}\n'.format(total=s['seen_episodes'])

                    sb = open(file, 'w')
                    sb.write(log_file)
                    sb.close()
                getShows(show_id, page+1)
        except Exception as e:
            print('Error: ', e)
    elif int(show_id[0]):
        serieId = int(show_id[0])
        urlApi = urlBase.format(method='show', token=access_token) + '&show_id={id}&include_episodes=1'.format(id=serieId)
        try:
            r = requests.get(urlApi)
            json_data = json.loads(r.content)
            if json_data['show']:
                dir_path = '{path}/{folder}'.format(path=path, folder='series')
                if not os.path.isdir(dir_path):
                    os.mkdir(dir_path)

                show = json_data['show']
                print(show)

                showName = formatName(show['name'])
                file = u'{dir}/{name}.md'.format(dir=dir_path, name=showName)

                sb = open(file, 'w')
                log_file = '# {name} ({number})\n\n'.format(name=showName, number=show['id'])
                log_file += '<img src="{}" width="250" />\n\n'.format(show['all_images']['poster']['0'])
                log_file += '## Status\n* {}\n'.format(show['status'])
                log_file += '## Last Aired\n* Season: {sesson}\n* Episode: {episode}\n'.format(sesson=show['last_aired']['season_number'], episode=show['last_aired']['number'])

                if show['last_seen']:
                    log_file += '## Last Seen\n* Season: {sesson}\n* Episode: {episode}\n'.format(sesson=show['last_seen']['season_number'], episode=show['last_seen']['number'])
                log_file += '## Seen Episodes\n* Total: {total}\n'.format(total=show['seen_episodes'])

                log_file += u'## Overview\n{txt}\n'.format(txt=show['overview'])
                log_file += '## Episodes\n'
                for e in show['episodes']:
                    log_file += u'1. {name} Season: {season} Episode: {episode}\n'.format(name=e['name'], season=e['season_number'], episode=e['number'])

                sb.write(log_file)
                sb.close()
        except Exception as e:
            print('Error: ', e)

def getEpisode(episode_id):
    print('El episode: ', episode_id)

def getShowTime(show_id):
    print('El tiempo de: ', show_id)

parser = argparse.ArgumentParser(description='Obtener datos de tu cuenta de TvTime')
parser.add_argument('-p', nargs=1, metavar='path', default='.', help='Carpeta donde almacenar el log')
parser.add_argument('-s', nargs=1, metavar='idShow', default='All', help='Guarda la(s) serie(s) y su progreso (último visto, ultimo emitido)')
parser.add_argument('-t', nargs='+', metavar='idShow', help='Tiempo que has visto una serie')
parser.add_argument('-e', nargs='+', metavar='idEpisode', help='Retorna datos de un episodeo')

args = parser.parse_args()
path = args.p
if args.e:
    getEpisode(args.e)
    exit()
if args.t:
    getShowTime(args.t)
    exit()

getShows(args.s)
