from datetime import datetime
import os
import requests
import json
import argparse

year = str(datetime.now().year)
week = str(datetime.now().sfrtime('%V'))
apikey = "ebb288a9fba45278c0b326b7766f8911"
user = "edgarkmarita"
method = {
    'track': '&method=user.gettoptracks&period=7day&limit=10',
    'artist': '&method=user.gettopartists&period=7day&limit=10',
    'album': '&method=user.gettopalbums&period=7day&limit=10',
}
lastfmApi = "http://ws.audioscrobbler.com/2.0/?user={usr}&api_key={api}&format=json".format(usr=user, api=apikey)

def topTen(path):
    try:
        url = lastfmApi + method['track']
        r = requests.get(url)
        json_data = json.loads(r.content)
        tracks = json_data['toptracks']['track']

        file = '{base}/{week}.md'.format(base=path, week=week)

        log_file = u'# El top Ten de la semana {}\n'.format(week)

        log_file += u'\n## Tracks\n'
        for t in tracks:
            log_file += u'1. {}, by: {}\n'.format(t['name'], t['artist']['name'])

        url_artist = lastfmApi + method['artist']
        r_artist = requests.get(url_artist)
        json_data_artist = json.loads(r_artist.content)
        artists = json_data_artist['topartists']['artist']

        log_file += u'\n## Artists\n'
        for a in artists:
            log_file += u'1. {}\n'.format(a['name'])

        url_album = lastfmApi + method['album']
        r_album = requests.get(url_album)
        json_data_album = json.loads(r_album.content)
        albums = json_data_album['topalbums']['album']

        log_file += u'\n## Albums\n'
        for al in albums:
            artista = u''
            if 'artist' in al:
                artista = u', by: {}'.format(al['artist']['name'])
            log_file += u'1. {}{}\n'.format(al['name'], artista)

        sb = open(file, 'w')
        sb.write(log_file)
    except Exception as e:
        print("Error: ",e)

parser = argparse.ArgumentParser(description='Obtenemos el top ten de la music escuchada.')
parser.add_argument('-p', '--path', action='store', default=False, help='Directorio donde almacena el log del top ten music')

args = parser.parse_args()
if not args.path:
    parse.print_help()
else:
    topTen(args.path)
