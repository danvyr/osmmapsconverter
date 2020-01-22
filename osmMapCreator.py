#!/usr/bin/python3.6

#TODO структура папки out
#TODO доставание полигонов из osm для любой страны (по админ уровню)
#TODO map rotate
#TODO сделать запуск локальный  
#TODO сделать запуск в докере
#TODO выбор какие карты и чем собирать с какими стилями и как резать.
#TODO текстовый гуи интерфейс для 
#TODO генерация json для приложения загрузки на android 
#TODO сделать тестовую замену name на name:be

import sys
import requests
import urllib.request
import os
import shutil





urls = {
    'osmandcreator': 'https://download.osmand.net/latest-night-build/OsmAndMapCreator-main.zip',
    'maps': 
        {'belarus': 'http://download.geofabrik.de/europe/belarus-latest.osm.pbf',
        
        }
}
currentDir = os.path.abspath( '.' )

currentMap = 'currentMap.txt'

inputDir = os.path.abspath('in')

polyDir = os.path.abspath('poly')
splitDir = os.path.abspath('split')
mapsmeDir = os.path.abspath('mapsme')

osmandDir = os.path.abspath('osmand')
OAMCDir  = osmandDir + '/OsmAndMapCreator'

outDir = os.path.abspath('out')
outOsmAnd = outDir + '/osmand'
outMapsme = outDir + '/mapsme'
outGarmin = outDir + '/garmin'



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

def prepare():
    #install
    try:
        os.system('sudo apt-get install osmctools')
    except:
        pass

    try:
        os.system('sudo apt-get install git qtbase5-dev cmake libsqlite3-dev clang libc++-dev libboost-iostreams-dev libglu1-mesa-dev python3-pip -y')
        os.chdir(mapsmeDir)
        os.system('git clone --depth=1 --recursive https://github.com/mapsme/omim.git')
        os.chdir(mapsmeDir + '/omim')
        os.system('./configure.sh')
        os.system('./tools/unix/build_omim.sh -sr generator_tool')
        os.chdir('tools/python/maps_generator')
        os.system('pip3 install -r requirements.txt')
        os.system('cp ' + mapsmeDir + '/map_generator.ini var/etc/map_generator.ini')
        os.chdir(currentDir)

    except:
        pass


    #prepare OSMAND
    try:
        url = urls['osmandcreator']
        resp = requests.head(url)        
        print("Last modified: " + resp.headers['last-modified'])
        pathToFile = osmandDir + '/' + 'OsmAndMapCreator-main.zip'
        urllib.request.urlretrieve(url,  pathToFile)
        os.system('unzip'+  pathToFile + ' -d ' + OAMCDir )
    except:
        pass

def clean():
    pass

def move():

    #check files in out folders and backup

    #move Osm

    for file in osmandDir:
        if file.endswith('.obf'):
            shutil.move(os.path.join(osmandDir, file), os.path.join(outOsmAnd, file))

def download():
    print ('Start downloading maps')
    try:
        for map_name, url_to_map in urls['maps'].items():
            print(map_name)
            resp = requests.head(url_to_map)        
            print("Last modified: " + resp.headers['last-modified'])  
            #pathToFile = os.path.join(inputDir,  map_name + '.osm.pbf')   # не работает     
            pathToFile = os.path.join(inputDir, map_name + '.osm.pbf')
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
                cmd= 'osmconvert ' + os.path.join(inputDir, mapFile) +' -B=' + os.path.join(polyDir, polyFile) + ' --complete-ways --complex-ways -o='+ os.path.join(splitDir, polyFile.replace('poly','pbf') ) +' --statistics'
                print (cmd)
                os.system(cmd)
        return 1
    except OSError as err:
        print("OS error: {0}".format(err))
        return 0
    except ValueError:
        print("Could not convert data to an integer.")
        return 0
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return 0

def osmand():
    try:
        os.chdir(osmandDir)
        #folder = 'OsmAndMapCreator'
        for mapFile in os.listdir(splitDir):
            mapFile = os.path.join(splitDir, mapFile )
            print(mapFile)

            cmd = 'java -Djava.util.logging.config.file="'+OAMCDir+'/logging.properties" \
                -Xms128M -Xmx3000M \
                -cp "'+OAMCDir+'/OsmAndMapCreator.jar:'+OAMCDir+'/lib/*.jar" net.osmand.MainUtilities generate-obf ' + mapFile
            os.system(cmd)
            
        os.chdir(currentDir)
        return 1

    except OSError as err:
        print("OS error: {0}".format(err))
        return 0
    except ValueError:
        print("Could not convert data to an integer.")
        return 0
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return 0
    
def mapsme():
    pass



def main():
    #if download():
    #     mapsme()
    #     if split():
    #         osmand()
        
    #split()
    #osmand()
    # mapsme()
    prepare()

if __name__ == '__main__':
    main()


