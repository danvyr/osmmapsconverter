#!/usr/bin/python3.6

#TODO структура папки out
#TODO map rotate
#TODO сделать запуск локальный  
#TODO сделать запуск в докере
#TODO выбор какие карты и чем собирать с какими стилями и как резать.
#TODO текстовый гуи интерфейс для 
#TODO 


import requests


urls = {
    'osmandcreator': 'https://download.osmand.net/latest-night-build/OsmAndMapCreator-main.zip',
    'maps': 
        {'belarus': 'http://download.geofabrik.de/europe/belarus-latest.osm.pbf',
        
        }
}

resp = requests.head(urls['maps']['belarus'])

print("Server: " + resp.headers['server'])
print("Last modified: " + resp.headers['last-modified'])
print("Content type: " + resp.headers['content-type'])
