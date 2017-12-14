# -*- coding: utf-8 -*-
from datetime import datetime, date
from lxml import html
import os
import requests
import json
import argparse
import re

year = datetime.now().strftime('%Y')
month = datetime.now().strftime('%m')
day = datetime.now().strftime('%d')
latsw = '10.335184845972135'
latne = '36.75538986899453'
lonsw = '-134.23095709375002'
lonne = '-74.86083990625002'
latneCel = '20.595880122078096'
lonneCel = '-100.7413277084961'
latswCel = '20.501365390433342'
lonswCel = '-100.97581714941407'
zoomCel = 13
catGas = 3
catHot = 2
zoomMap = 5
urlPronostico = "http://pronosticodemanda.pemex.com/WS_GP_2/Pemex.Servicios.svc/web/get_Est_Reg?callback=jQuery111004208794787871024_1484250912002&latne={latne}&lonne={lonne}&latsw={latsw}&lonsw={lonsw}&z={zoom}&category={cat}&_=1484250912004".format(latne=latne, lonne=lonne, latsw=latsw, lonsw=lonsw, cat=catGas, zoom=zoomMap)
urlPronosticoCel = "http://pronosticodemanda.pemex.com/WS_GP_2/Pemex.Servicios.svc/web/get_Est_Reg?callback=jQuery111004208794787871024_1484250912002&latne={latne}&lonne={lonne}&latsw={latsw}&lonsw={lonsw}&z={zoom}&category={cat}&_=1484250912004".format(latne=latneCel, lonne=lonneCel, latsw=latswCel, lonsw=lonswCel, cat=catGas, zoom=zoomCel)
estacion = 'http://guiapemex.pemex.com/Paginas/DetalleGas.aspx?val={id}&GetFrag=1'
precioGeneral = {
    'max': {
        'magna': {
            'estacion': '',
            'precio': 0,
            'direccion': '',
        },
        'premium': {
            'estacion': '',
            'precio': 0,
            'direccion': '',
        },
        'diesel': {
            'estacion': '',
            'precio': 0,
            'direccion': '',
        },
    },
    'min': {
        'magna': {
            'estacion': '',
            'precio': 999,
            'direccion': '',
        },
        'premium': {
            'estacion': '',
            'precio': 999,
            'direccion': '',
        },
        'diesel': {
            'estacion': '',
            'precio': 999,
            'direccion': '',
        },
    },
    'celaya': {
        'max': {
            'magna': {
                'estacion': '',
                'precio': 0,
                'direccion': '',
            },
            'premium': {
                'estacion': '',
                'precio': 0,
                'direccion': '',
            },
            'diesel': {
                'estacion': '',
                'precio': 0,
                'direccion': '',
            },
        },
        'min': {
            'magna': {
                'estacion': '',
                'precio': 999,
                'direccion': '',
            },
            'premium': {
                'estacion': '',
                'precio': 999,
                'direccion': '',
            },
            'diesel': {
                'estacion': '',
                'precio': 999,
                'direccion': '',
            },
        }
    }
}
estacionesCelaya = ["E09484", "E05592", "E04669", "E04684", "E04047", "E12061", "E04670", "E12268", "E08302", "E07969", "E09868", "E05708", "E08852", "E04293", "E02849", "E03894", "E09714", "E05238", "E07995", "E04370", "E04977", "E07183", "E04249", "E00383", "E03294", "E10195", "E12093", "E00384", "E08462", "E07996", "E04168", "E11961", "E10216", "E07174", "E08157", "E08412", "E11310", "E08229", "E04044", "E03179", "E04068", "E10570", "E11513", "E00385", "E03135", "E04513", "E11220", "E12398", "E00386", "E10740", "E00390", "E12709", "E12912", "E12813", "E12845", "E00391", "E09966", "E09936", "E10617", "E13042", "E05630", "E10128", "E03987"]

def get_price(id):
    precios = {
        'id': '',
        'magna': 0,
        'premium' : 0,
        'diesel': 0,
        'direccion': ''
    }

    try:
        p = requests.get(estacion.format(id=id))
        tree = html.fromstring(p.content)
        magna = tree.xpath('//div[@id="magna"]/p[@class="price"]/text()')
        premium = tree.xpath('//div[@id="premium"]/p[@class="price"]/text()')
        diesel = tree.xpath('//div[@id="diesel"]/p[@class="price"]/text()')
        direccion = tree.xpath('//div[@id="info"]/p[@class="address"]/text()')
        if len(magna) > 0:
            precios['magna'] = float(magna[0][1:])
        if len(premium) > 0:
            precios['premium'] = float(premium[0][1:])
        if len(diesel) > 0:
            precios['diesel'] = float(diesel[0][1:])
        precios['direccion'] = direccion[0]
        precios['id'] = id
    except Exception as e:
        print 'Error: ', e

    return precios

def log(path):
    try:
        file = '{base}/{day}.md'.format(base=path, day=day)
        log_file = u'# Precios del combustible en México {day}/{month}/{year} :car:\n\n## Gasolineras que debemos evitar :cold_sweat:\n1. ### Magna\n  * **Nombre:** {maxMagnaNombre}\n  * **Dirección:** {maxMagnaDireccion}\n  * **Precio:** $ {maxMagnaPrecio}\n\n1. ### Premium\n  * **Nombre:** {maxPremiumNombre}\n  * **Dirección:** {maxPremiumDireccion}\n  * **Precio:** $ {maxPremiumPrecio}\n\n1. ### Diesel\n  * **Nombre:** {maxDieselNombre}\n  * **Dirección:** {maxDieselDireccion}\n  * **Precio:** $ {maxDieselPrecio}\n\n\n## Gasolineras que debemos ir :wink:\n1. ### Magna\n  * **Nombre:** {minMagnaNombre}\n  * **Dirección:** {minMagnaDireccion}\n  * **Precio:** $ {minMagnaPrecio}\n\n1. ### Premium\n  * **Nombre:** {minPremiumNombre}\n  * **Dirección:** {minPremiumDireccion}\n  * **Precio:** $ {minPremiumPrecio}\n\n1. ### Diesel\n  * **Nombre:** {minDieselNombre}\n  * **Dirección:** {minDieselDireccion}\n  * **Precio:** $ {minDieselPrecio}\n\n\n## En Celaya\n1. ### Max. Magna\n  * **Nombre:** {celayaMaxMagnaNombre}\n  * **Dirección:** {celayaMaxMagnaDireccion}\n  * **Precio:** $ {celayaMaxMagnaPrecio}\n\n1. ### Max. Premium\n  * **Nombre:** {celayaMaxPremiumNombre}\n  * **Dirección:** {celayaMaxPremiumDireccion}\n  * **Precio:** $ {celayaMaxPremiumPrecio}\n\n1. ### Max. Diesel\n  * **Nombre:** {celayaMaxDieselNombre}\n  * **Dirección:** {celayaMaxDieselDireccion}\n  * **Precio:** $ {celayaMaxDieselPrecio}\n\n1. ### Min. Magna\n  * **Nombre:** {celayaMinMagnaNombre}\n  * **Dirección:** {celayaMinMagnaDireccion}\n  * **Precio:** $ {celayaMinMagnaPrecio}\n\n1. ### Min. Premium\n  * **Nombre:** {celayaMinPremiumNombre}\n  * **Dirección:** {celayaMinPremiumDireccion}\n  * **Precio:** $ {celayaMinPremiumPrecio}\n\n1. ### Min. Diesel\n  * **Nombre:** {celayaMinDieselNombre}\n  * **Dirección:** {celayaMinDieselDireccion}\n  * **Precio:** $ {celayaMinDieselPrecio}'.format(day=day, month=month, year=year, maxMagnaNombre=precioGeneral['max']['magna']['estacion'], maxMagnaDireccion=precioGeneral['max']['magna']['direccion'], maxMagnaPrecio=precioGeneral['max']['magna']['precio'], maxPremiumNombre=precioGeneral['max']['premium']['estacion'], maxPremiumDireccion=precioGeneral['max']['premium']['direccion'], maxPremiumPrecio=precioGeneral['max']['premium']['precio'], maxDieselNombre=precioGeneral['max']['diesel']['estacion'], maxDieselDireccion=precioGeneral['max']['diesel']['direccion'], maxDieselPrecio=precioGeneral['max']['diesel']['precio'], minMagnaNombre=precioGeneral['min']['magna']['estacion'], minMagnaDireccion=precioGeneral['min']['magna']['direccion'], minMagnaPrecio=precioGeneral['min']['magna']['precio'], minPremiumNombre=precioGeneral['min']['premium']['estacion'], minPremiumDireccion=precioGeneral['min']['premium']['direccion'], minPremiumPrecio=precioGeneral['min']['premium']['precio'], minDieselNombre=precioGeneral['min']['diesel']['estacion'], minDieselDireccion=precioGeneral['min']['diesel']['direccion'], minDieselPrecio=precioGeneral['min']['diesel']['precio'], celayaMaxMagnaNombre=precioGeneral['celaya']['max']['magna']['estacion'], celayaMaxMagnaDireccion=precioGeneral['celaya']['max']['magna']['direccion'], celayaMaxMagnaPrecio=precioGeneral['celaya']['max']['magna']['precio'], celayaMaxPremiumNombre=precioGeneral['celaya']['max']['premium']['estacion'], celayaMaxPremiumDireccion=precioGeneral['celaya']['max']['premium']['direccion'], celayaMaxPremiumPrecio=precioGeneral['celaya']['max']['premium']['precio'], celayaMaxDieselNombre=precioGeneral['celaya']['max']['diesel']['estacion'], celayaMaxDieselDireccion=precioGeneral['celaya']['max']['diesel']['direccion'], celayaMaxDieselPrecio=precioGeneral['celaya']['max']['diesel']['precio'], celayaMinMagnaNombre=precioGeneral['celaya']['min']['magna']['estacion'], celayaMinMagnaDireccion=precioGeneral['celaya']['min']['magna']['direccion'], celayaMinMagnaPrecio=precioGeneral['celaya']['min']['magna']['precio'], celayaMinPremiumNombre=precioGeneral['celaya']['min']['premium']['estacion'], celayaMinPremiumDireccion=precioGeneral['celaya']['min']['premium']['direccion'], celayaMinPremiumPrecio=precioGeneral['celaya']['min']['premium']['precio'], celayaMinDieselNombre=precioGeneral['celaya']['min']['diesel']['estacion'], celayaMinDieselDireccion=precioGeneral['celaya']['min']['diesel']['direccion'], celayaMinDieselPrecio=precioGeneral['celaya']['min']['diesel']['precio']).encode('utf-8')
        sb = open(file, 'w')
        sb.write(log_file)
    except Exception as e:
        print 'Error: ',e


def getEstaciones(url):
    json_data = {}
    try:
        r = requests.get(url)
        jsond = r.content[42:]
        jsond = jsond[:len(jsond) - 2]
        json_data = json.loads(jsond)
    except Exception as e:
        print 'Error get: ',e

    return json_data

def estaciones(path):
    estacion_array = []
    try:
        json_data = getEstaciones(urlPronostico)
        for e in json_data:
            if int(e['active']) == 1:
                estacion_array.append({
                    'id': e['id'],
                    'nombre': e['place_name'],
                    'lat': e['place_latitude'],
                    'lng': e['place_longitude']
                })

        json_data = getEstaciones(urlPronosticoCel)
        for e in json_data:
            if int(e['active']) == 1:
                estacion_array.append({
                    'id': e['id'],
                    'nombre': e['place_name'],
                    'lat': e['place_latitude'],
                    'lng': e['place_longitude']
                })

        if len(estacion_array) > 0:
            for es in estacion_array:
                precios = get_price(es['id'])
                # En el pais
                if precioGeneral['max']['magna']['precio'] < precios['magna']:
                    precioGeneral['max']['magna']['precio'] = precios['magna']
                    precioGeneral['max']['magna']['estacion'] = es['nombre']
                    precioGeneral['max']['magna']['direccion'] = precios['direccion']
                if precioGeneral['min']['magna']['precio'] > precios['magna'] and precios['magna'] > 0:
                    precioGeneral['min']['magna']['precio'] = precios['magna']
                    precioGeneral['min']['magna']['estacion'] = es['nombre']
                    precioGeneral['min']['magna']['direccion'] = precios['direccion']

                if precioGeneral['max']['premium']['precio'] < precios['premium']:
                    precioGeneral['max']['premium']['precio'] = precios['premium']
                    precioGeneral['max']['premium']['estacion'] = es['nombre']
                    precioGeneral['max']['premium']['direccion'] = precios['direccion']
                if precioGeneral['min']['premium']['precio'] > precios['premium'] and precios['premium'] > 0:
                    precioGeneral['min']['premium']['precio'] = precios['premium']
                    precioGeneral['min']['premium']['estacion'] = es['nombre']
                    precioGeneral['min']['premium']['direccion'] = precios['direccion']

                if precioGeneral['max']['diesel']['precio'] < precios['diesel']:
                    precioGeneral['max']['diesel']['precio'] = precios['diesel']
                    precioGeneral['max']['diesel']['estacion'] = es['nombre']
                    precioGeneral['max']['diesel']['direccion'] = precios['direccion']
                if precioGeneral['min']['diesel']['precio'] > precios['diesel'] and precios['diesel'] > 0:
                    precioGeneral['min']['diesel']['precio'] = precios['diesel']
                    precioGeneral['min']['diesel']['estacion'] = es['nombre']
                    precioGeneral['min']['diesel']['direccion'] = precios['direccion']

                # En Celaya
                if es['id'] in estacionesCelaya:
                    if precioGeneral['celaya']['max']['magna']['precio'] < precios['magna']:
                        precioGeneral['celaya']['max']['magna']['precio'] = precios['magna']
                        precioGeneral['celaya']['max']['magna']['estacion'] = es['nombre']
                        precioGeneral['celaya']['max']['magna']['direccion'] = precios['direccion']
                    if precioGeneral['celaya']['min']['magna']['precio'] > precios['magna'] and precios['magna'] > 0:
                        precioGeneral['celaya']['min']['magna']['precio'] = precios['magna']
                        precioGeneral['celaya']['min']['magna']['estacion'] = es['nombre']
                        precioGeneral['celaya']['min']['magna']['direccion'] = precios['direccion']
                    if precioGeneral['celaya']['max']['premium']['precio'] < precios['premium']:
                        precioGeneral['celaya']['max']['premium']['precio'] = precios['premium']
                        precioGeneral['celaya']['max']['premium']['estacion'] = es['nombre']
                        precioGeneral['celaya']['max']['premium']['direccion'] = precios['direccion']
                    if precioGeneral['celaya']['min']['premium']['precio'] > precios['premium'] and precios['premium'] > 0:
                        precioGeneral['celaya']['min']['premium']['precio'] = precios['premium']
                        precioGeneral['celaya']['min']['premium']['estacion'] = es['nombre']
                        precioGeneral['celaya']['min']['premium']['direccion'] = precios['direccion']
                    if precioGeneral['celaya']['max']['diesel']['precio'] < precios['diesel']:
                        precioGeneral['celaya']['max']['diesel']['precio'] = precios['diesel']
                        precioGeneral['celaya']['max']['diesel']['estacion'] = es['nombre']
                        precioGeneral['celaya']['max']['diesel']['direccion'] = precios['direccion']
                    if precioGeneral['celaya']['min']['diesel']['precio'] > precios['diesel'] and precios['diesel'] > 0:
                        precioGeneral['celaya']['min']['diesel']['precio'] = precios['diesel']
                        precioGeneral['celaya']['min']['diesel']['estacion'] = es['nombre']
                        precioGeneral['celaya']['min']['diesel']['direccion'] = precios['direccion']
            log(path)
    except Exception as e:
        print 'Error: ',e

parser = argparse.ArgumentParser(description='Se obtiene el precio de combustible en Mexico segun PEMEX.')
parser.add_argument('-P', '--path', action='store', default=False, help='Carpeta donde almacena el log de precios')

args = parser.parse_args()

if not args.path:
    parser.print_help()
else:
    estaciones(args.path)