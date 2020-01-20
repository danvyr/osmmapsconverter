#!/usr/bin/python3.6

#TODO структура папки out
#TODO map rotate
#TODO сделать запуск локальный  
#TODO сделать запуск в докере
#TODO выбор какие карты и чем собирать с какими стилями и как резать.
#TODO текстовый гуи интерфейс для 
#TODO сделать тестовую замену name на name:be

import sys
import requests
import urllib.request
import os
from os import listdir
from os.path import isfile, join
from os import walk



urls = {
    'osmandcreator': 'https://download.osmand.net/latest-night-build/OsmAndMapCreator-main.zip',
    'maps': 
        {'belarus': 'http://download.geofabrik.de/europe/belarus-latest.osm.pbf',
        
        }
}
polyDir = 'poly'
inputDir = 'in'
splitDir = 'split'

currentMap = 'currentMap.txt'


def checkVerstion():
    #наверное не надо
    version = ''
    try:
        with open(currentMap, 'r') as cf:
            version = cf.readline()
    except:
        with open(currentMap, 'w') as cf:
            cf.write(version)
    return 1
    


def download():
    print ('Start downloading')
    try:
        for map_name, url_to_map in urls['maps'].items():
            print(map_name)
            resp = requests.head(url_to_map)        
            print("Last modified: " + resp.headers['last-modified'])  
            #pathToFile = os.path.join(inputDir,  map_name + '.osm.pbf')   # не работает     
            pathToFile = inputDir + '/' + map_name + '.osm.pbf'
            print (pathToFile)
            urllib.request.urlretrieve(url_to_map,  pathToFile)            
            print ('all downloaded')
            return 1
    except:
        return 0


def split():
    try:
        for mapFile in os.listdir(inputDir):
            print(mapFile)
            for polyFile in os.listdir(polyDir):
                print(polyFile)
                cmd= 'osmconvert ' + inputDir +'/' + mapFile +' -B=' + polyDir +'/' + polyFile + ' --complete-ways --complex-ways -o='+ splitDir + '/' + polyFile.replace('poly','pbf') +' --statistics'
                print (cmd)
                os.system(cmd)
        return 1
    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except:
        print("Unexpected error:", sys.exc_info()[0])

def osmand():
    pass

def mapsme():
    pass



def main():
    #if download():
    #     mapsme()
    #     if split():
    #         osmand()
        
    split()

if __name__ == '__main__':
    main()


