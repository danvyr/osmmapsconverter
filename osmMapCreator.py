#!/usr/bin/python3.6

#TODO структура папки out
#TODO map rotate
#TODO сделать запуск локальный  
#TODO сделать запуск в докере
#TODO выбор какие карты и чем собирать с какими стилями и как резать.
#TODO текстовый гуи интерфейс для 
#TODO 

import sys
import requests
import urllib.request


in_dir = 'in'
urls = {
    'osmandcreator': 'https://download.osmand.net/latest-night-build/OsmAndMapCreator-main.zip',
    'maps': 
        {'belarus': 'http://download.geofabrik.de/europe/belarus-latest.osm.pbf',
        
        }
}



def osmand():
    pass

def mapsme():
    pass

def split():
    return 1

def download():
    for map_name, url_to_map in urls['maps']:
        resp = requests.head(url_to_map)        
        print("Last modified: " + resp.headers['last-modified'])


        urllib.request.urlretrieve(url_to_map, in_dir + map_name)
        return 1


def main():
    if download():
        mapsme()
        if split():
            osmand()
        





    


if __name__ == '__main__':
    main()


