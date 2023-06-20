#!/usr/bin/env python3

# TODO формировать json и xml(osm_downloader format) с датой создания файлов и путями скачивания

# TODO доставание полигонов из osm для любой страны (по админ уровню) или использование полигонов organicmap
# TODO сделать тестовую замену name на name:be
# TODO общий in, для разных приложения, с датой скачивания
# TODO раскидать по модулям ?


import logging
import sys
import requests
import urllib.request
import os
import shutil
import glob
import datetime
import email.utils as eut
import multiprocessing
from datetime import datetime, date, time
from multiprocessing import Pool
# from multiprocessing.dummy import Pool as ThreadPool

from multiprocessing import cpu_count
from enum import Enum

class statuses(Enum):
    running = "running"
    finished = "finished"


MAPS_BUILD_DEF = "/home/osm/dev/osmmapsconverter/organicmap/map_build"

urls = {
    'osmandcreator': 'https://download.osmand.net/latest-night-build/OsmAndMapCreator-main.zip',
    'maps':
        {'belarus': 'http://download.geofabrik.de/europe/belarus-latest.osm.pbf',

         }
}
#organicmap_maps='Belarus_Brest Region Belarus_Homiel Region Belarus_Hrodna Region Belarus_Maglieu Region Belarus_Minsk Region Belarus_Vitebsk Region'
organicmap_maps=[
             'Belarus_Minsk Region',
             'Belarus_Brest Region',
             'Belarus_Homiel Region',
             'Belarus_Hrodna Region',
             'Belarus_Maglieu Region',
             'Belarus_Vitebsk Region'
            ]
countries = [
    ["Belarus*",
        "http://download.geofabrik.de/europe/belarus-latest.osm.pbf"],
#    ["Ukraine*",
#        "http://download.geofabrik.de/europe/ukraine-latest.osm.pbf"],

#    ["Poland*",
#        "http://download.geofabrik.de/europe/poland-latest.osm.pbf"],

    ["Poland_Lower Silesian Voivodeship",
        "http://download.geofabrik.de/europe/poland/dolnoslaskie-latest.osm.pbf"],
    ["Poland_Masovian Voivodeship",
        "http://download.geofabrik.de/europe/poland/mazowieckie-latest.osm.pbf"],
    ["Poland_Kuyavian-Pomeranian Voivodeship",
        "http://download.geofabrik.de/europe/poland/kujawsko-pomorskie-latest.osm.pbf"],
    ["Poland_Lodz Voivodeship",
        "http://download.geofabrik.de/europe/poland/lodzkie-latest.osm.pbf"],
    ["Poland_Lublin Voivodeship",
        "http://download.geofabrik.de/europe/poland/lubelskie-latest.osm.pbf"],
    ["Poland_Lubusz Voivodeship",
        "http://download.geofabrik.de/europe/poland/lubuskie-latest.osm.pbf"],
    ["Poland_Lesser Poland Voivodeship",
        "http://download.geofabrik.de/europe/poland/malopolskie-latest.osm.pbf"],
    ["Poland_Opole Voivodeship",
        "http://download.geofabrik.de/europe/poland/opolskie-latest.osm.pbf"],
    ["Poland_Subcarpathian Voivodeship",
        "http://download.geofabrik.de/europe/poland/podkarpackie-latest.osm.pbf"],
    ["Poland_Podlaskie Voivodeship",
        "http://download.geofabrik.de/europe/poland/podlaskie-latest.osm.pbf"],
    ["Poland_Pomeranian Voivodeship",
        "http://download.geofabrik.de/europe/poland/pomorskie-latest.osm.pbf"],
    ["Poland_Silesian Voivodeship",
        "http://download.geofabrik.de/europe/poland/slaskie-latest.osm.pbf"],
    ["Poland_Swietokrzyskie Voivodeship",
        "http://download.geofabrik.de/europe/poland/swietokrzyskie-latest.osm.pbf"],
    ["Poland_Warmian-Masurian Voivodeship",
        "http://download.geofabrik.de/europe/poland/warminsko-mazurskie-latest.osm.pbf"],
    ["Poland_Greater Poland Voivodeship",
        "http://download.geofabrik.de/europe/poland/wielkopolskie-latest.osm.pbf"],
    ["Poland_West Pomeranian Voivodeship",
        "http://download.geofabrik.de/europe/poland/zachodniopomorskie-latest.osm.pbf"],

]

user = 'osm'
javaOpt = ' -Xms256M -Xmx4000M '

currentDir = os.path.abspath('.')
currentMap = os.path.join(currentDir, 'currentMap.txt')
currentStatus = os.path.join(currentDir, 'status.txt')

inputDir = os.path.abspath('/var/www/maps/pbf')

polyDir = os.path.abspath('poly')
splitDir = os.path.abspath('split')
logsDir = os.path.abspath('logs')

organicmapDir = os.path.abspath('organicmap')
osmandDir = os.path.abspath('osmand')
garminDir = os.path.abspath('garmin')

OAMCDir = os.path.join(osmandDir, 'OsmAndMapCreator')

tempGarmin = os.path.join(garminDir, 'temp')
tempOutGarmin = os.path.join(garminDir, 'out')
tempOrganicmap = os.path.join(organicmapDir, 'map_build')
tempSplit = os.path.join(currentDir, 'split')

# in  organicmap/omim/tools/python/maps_generator/var/etc/map_generator.ini MAIN_OUT_PATH: <full_path>/organicmap/temp

outDir = os.path.join('/var/www/maps')
outOsmAnd = os.path.join(outDir, 'osmand')
outOrganicmaps = os.path.join(outDir, 'organicmap')
outGarmin = os.path.join(outDir, 'garmin')

tempDirs = [tempOrganicmap, tempGarmin, tempOutGarmin, tempSplit]
innerDirs = [polyDir, splitDir, organicmapDir, osmandDir, garminDir, OAMCDir, logsDir]
outDirs = [outDir, outOsmAnd, outOrganicmaps, outGarmin]

moveCount = 0



logfile = os.path.join(logsDir, 'osmmapcreator_' + str(datetime.today().strftime('%Y-%m-%d_%H-%M-%S')) + '.log')
logging.basicConfig(filename=logfile, level=logging.INFO)


def run_command(command):
    log (command)
    os.system(command)


def run_docker(command):
    log("[INFO] RUN COMAND ****************************** " + command[0])
    os.system("docker rm "+ command[2])
    print (command[0])
    logging.info(str(command))
    os.system(command[0])
    os.system("rm -rf "+ command[2])
    os.system("docker rm "+ command[2])
    log("[INFO] END COMAND ******************************" + command[0])

def nowtime():
    return datetime.today().strftime('%H-%M-%S: ')

def log(status):
    s = nowtime() + status
    print(s)
    logging.info(s)


def readStatus():
    try:
        with open(currentStatus, 'r') as f:
            statusLine = f.readline()
            log ('[INFO] currentStatus  '+ statusLine)
            return statusLine
    except:
        with open(currentStatus, 'w') as f:
            log ('[INFO] except, write start')
            f.write('start')
        return 'finished'

def writeStatus(status):
    try:
        with open(currentStatus, 'w') as f:
            f.write(status)
            return 1
    except:
        return 0



def checkVersion(urlDate):
    # наверное не надо
    # version = ""
    log ('[INFO] checkVersion urlDate')
    try:
        with open(currentMap, 'r') as vf:
            version = vf.readline()
            if version != urlDate:
                log ('[INFO] checkVersion not match')
                return 1
            else:
                log ('[INFO] checkVersion match. Skip')
                return 0
    except:
        log ('[INFO] first launch')
        return 1


def writeVersion(urlDate):
    try:
        with open(currentMap, 'w') as vf:
            vf.write(urlDate)
    except:
        log('can\'t write version file')


def checkDirs():
    for folder in (*innerDirs, *outDirs, *tempDirs ):
        if not os.path.isdir(folder):
            try:
                os.mkdir(folder)
            except:
                os.system('sudo mkdir -p ' + folder)
                os.system('sudo chown ' + user + ':' + user + ' ' + folder)


def prepare():
    checkDirs()
    log('prepare')

    # install
    try:
        log('install osmctools')
        os.system('sudo apt-get install osmctools')
    except:
        pass


    # prepare OSMAND
    try:
        log('install osmandMapCreator')

        url = urls['osmandcreator']
        resp = requests.head(url)
        logging.info("Last modified: " + resp.headers['last-modified'])
#        log("Last modified: " + resp.headers['last-modified'])
        pathToFile = os.path.join(osmandDir, 'OsmAndMapCreator-main.zip')
        urllib.request.urlretrieve(url,  pathToFile)
        os.system('unzip ' + pathToFile + ' -d ' + OAMCDir)
    except:
        pass

    # prepare Garmin
    os.chdir(garminDir)
    os.system('bash prepare.sh')
    os.chdir(currentDir)


def clean():
    log ('Clean folders:')
    log(str(tempDirs))

    for folder in tempDirs:
        log(folder)
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if (os.path.isfile(file_path) or os.path.islink(file_path)) and filename != '.gitignore':
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                log('Failed to delete %s. Reason: %s' % (file_path, e))

    #osmconvert_tempfile
    for filename in os.listdir(currentDir):
        file_path = os.path.join(currentDir, filename)
        try:
            if (os.path.isfile(file_path) or os.path.islink(file_path)) and filename.find('osmconvert_tempfile') > -1:
                os.unlink(file_path)
        except Exception as e:
            log('Failed to delete %s. Reason: %s' % (file_path, e))


def moveOrganicmaps():

    organicmapsCount = 0
    global moveCount
    log('find mapme maps')
    # find mapme maps
    path = ''
    status = False
    for folder in os.listdir(tempOrganicmap):
        dirL1 = os.path.join(tempOrganicmap, folder)
        if (folder.find('20') > -1) and os.path.isdir(dirL1):
            log(dirL1)
            t = folder[2:10].replace('_','')
            log(t)
            dirL2 = os.path.join(dirL1, t)
            log(dirL2)
            if os.path.isdir(dirL2):
                os.chdir(dirL2)
                log(dirL2)
                status_file = os.path.join(dirL1, 'status/stages.status')
                log(status_file)
                with open(status_file, 'r') as f:
                    str = f.readline()
                    log('Status ')
                    log(str)
                    if str == 'finish':
                        status = True
                        path = dirL2
                        log(path)
            os.chdir(tempOrganicmap)

    # moving Organicmaps maps
    if status:
        log('move Organicmaps map')
        for file in os.listdir(path):
            if file.endswith('.mwm'):
                logging.info(file)
                shutil.move(os.path.join(path, file),
                            os.path.join(outOrganicmaps, file))
                organicmapsCount = organicmapsCount + 1
    else:
        log('Not move Organicmaps map')
    os.chdir(currentDir)
    moveCount = moveCount + organicmapsCount

    return organicmapsCount


def moveOsmand():
    osmandCount = 0
    global moveCount
    # move OsmAnd maps
    log('move OsmAND map')
    for file in os.listdir(osmandDir):
        if file.endswith('.obf'):
            log(file)
            shutil.move(os.path.join(osmandDir, file),
                        os.path.join(outOsmAnd, file))
            osmandCount = osmandCount + 1
    moveCount = moveCount + osmandCount
    return osmandCount


def moveGarmin():
    global moveCount
    garminCount = 0
    # move garmin temp/Belarus_map_general.img
    log('move garmin map')
    try:
        name = 'Belarus_*'
        path = tempOutGarmin + '/' + name
        print ("[INFO] Garmin temp out path = " + path)
        print ("[INFO] Garmin out path = " + outGarmin)
        for file in glob.glob(path):
            print("[INFO] Moving file " + file)
            shutil.move(file, outGarmin)
            garminCount = garminCount + 1
    except:
        log('no garmin map')

    moveCount = moveCount + garminCount
    return garminCount


def checkURL():

    log('Cheking maps urls')
    try:
        for map_name, url_to_map in urls['maps'].items():
            log(map_name)
            resp = requests.head(url_to_map)
            urlLastModified = resp.headers['last-modified']
            log (urlLastModified)
            urlRawDate = eut.parsedate(urlLastModified)
            log("urlRawDate " +  str(urlRawDate))
            urlDate  =  datetime(*urlRawDate[:6])
            log("Last modified: " + str(urlDate.isoformat() ) )
            return str(urlDate.isoformat())

    except:
        log('Checking failed')
        log("Unexpected error:"+ sys.exc_info()[0])

        return '0'


def download():

    log('Start downloading maps')
    try:
        for map_name, url_to_map in urls['maps'].items():
            log(map_name)
            pathToFile = os.path.join(inputDir, map_name + '.osm.pbf')
            log(pathToFile)
            if urllib.request.urlretrieve(url_to_map,  pathToFile):
                log('all downloaded')
                return 1
            else:
                return 0

    except:
        log('downloading failed')
        log("Unexpected error:"+ sys.exc_info()[0])
        return 0


def split():
    pool = Pool(cpu_count())

    log('Start split')
    try:
        cmds = []
        for map_name, url_to_map in urls['maps'].items():
            mapFile = os.path.join(inputDir, map_name + '.osm.pbf')
            log(mapFile)
            for polyFile in os.listdir(polyDir):
                log(polyFile)
                cmd = 'osmconvert ' + os.path.join(inputDir, mapFile) + ' -B=' + '"' + os.path.join(polyDir, polyFile) + '"' \
                    + ' --complete-ways --complex-ways -o='  \
                    + '"' + os.path.join(splitDir, polyFile.replace('poly', 'pbf')) + '"'   \
                    + ' --statistics'
                cmds.append(cmd)

        pool.map(run_command, cmds)
        pool.close()
        pool.join()
        log('Finish split')
        return 1

    except OSError as err:
        log("OS error: {0}".format(err))
        return 0
    except ValueError:
        log("Could not convert data to an integer.")
        return 0
    except:
        log("Unexpected error:"+ sys.exc_info()[0])
        return 0


def osmand():
    log('Start OSMAND map Creator')
    try:
        os.chdir(osmandDir)
        for mapFile in os.listdir(splitDir):
            mapFile = os.path.join(splitDir, mapFile)
            log(mapFile)

            cmd = 'java -Djava.util.logging.config.file="'+OAMCDir+'/logging.properties"' + javaOpt + '-cp "'+OAMCDir+'/OsmAndMapCreator.jar:'+OAMCDir+'/lib/*.jar" net.osmand.MainUtilities generate-obf ' \
                + '"' + mapFile + '"'
            log(cmd)
            os.system(cmd)

        log('Finish OSMAND map Creator')

        os.chdir(currentDir)
        moveOsmand()
        return 1

    except OSError as err:
        log("OS error: {0}".format(err))
        return 0
    except ValueError:
        log("Could not convert data to an integer.")
        return 0
    except:
        log("Unexpected error:"+ sys.exc_info()[0])
        return 0

def organicmaps():
    print("[INFO] organicmaps")
    cmd_rm = "docker rm /organicmap_mapgenerator "
    print("[INFO] organicmaps pool")
    pool = Pool(2) #cpu_count())
    try:
        cmds = []
        i=0
        for map_name, map_url in countries:
            print(map_name + " " + map_url)
            MAPS_BUILD=MAPS_BUILD_DEF + '/' + str(i)
            CONTAINER_NAME="oranic_generator_"+ str(i)
            os.system("mkdir -p "+ MAPS_BUILD)

            cmd = "docker run   " + \
            "--mount type=bind,source=" + MAPS_BUILD + ",target=/organicmaps/maps_build " + \
            "--mount type=bind,source="+ outOrganicmaps +",target=/organicmaps/out " + \
            "-e PLANET_URL='" + map_url + "'  " + \
            "-e PLANET_MD5_URL='" + map_url + ".md5' " + \
            "-e ORGANICMAP_COUNTRIES='" + map_name + "' " + \
            "-e ORGANICMAP_SKIP='Coastline,MwmStatistics' " + \
            "-e THREADS_COUNT=" + "2" + " " \
            "--name " + CONTAINER_NAME + " danvyr/organicmap:latest"
            print(cmd)
            cmds.append([cmd, MAPS_BUILD, CONTAINER_NAME])
            i+=1
#            "-e SUBWAY_URL='https://download.openstreetmap.by/subway.json'  " + \

        logging.info(str(cmds))

        print (cmds)
        print ("START")
        pool.map(run_docker, cmds)
        pool.close()
        pool.join()

    except OSError as err:
        log("OS error: {0}".format(err))
        return 0
    except ValueError:
        log("Could not convert data to an integer.")
        return 0
    except:
        log("Unexpected error:"+ sys.exc_info()[0])
        return 0


# def organicmaps():
#     log('Start OrganicMaps map Creator')
#     os.chdir(organicmapDir)
#     os.system('bash generate_map.sh')
#     moveOrganicmaps()
#     clean()
#     # for map in organicmap_maps:
#     #     log('Start ' + str(map))
#     #     os.chdir(os.path.join(organicmapDir, 'omim/tools/python'))

#     os.chdir(currentDir)
#     log('Finish OrganicMaps maps')


def garmin():
    log('Start GARMIN map Creator')
    os.chdir(garminDir)
    for map_name, url_to_map in urls['maps'].items():
        mapFile = os.path.join(inputDir, map_name + '.osm.pbf')
        os.system('bash build.sh ' + mapFile)
    os.chdir(currentDir)
    log('Finish GARMIN map Creator')

    moveGarmin()

def convertRus():
    log('Convert rus')
    for map_name, url_to_map in urls['maps'].items():
        log(map_name)
        pathToFile = os.path.join(inputDir, map_name + '.osm.pbf')
        pathToRuFile = os.path.join(inputDir, map_name + '-ru.osm.pbf')
        os.system('python3 rus/osm_back.py -l ru -o ' + pathToRuFile + ' ' + pathToFile)
    log('END convert rus')




def main():
 #   prepare():
    log('Started')
    dl = checkURL()
    log ('Check version = '+ dl)
    checkVersion(dl)
    if (readStatus() == 'finished'):
        if checkVersion(dl):
            writeStatus('running')
            checkDirs()
            log('Run ')
            writeStatus('running')
            if(download()):
                log('downloaded')
                convertRus()
                if split():
                    osmand()
                garmin()
            organicmaps()
            if(moveCount > 1):
                writeVersion(dl)
                log('Something done')
            else:
                log('Nothing done')
            clean()
            writeStatus('finished')
        else:
            log('Can\'t start - updated')

    else:
        log('Can\'t start - check status file')
    log('Finished')


if __name__ == '__main__':
    main()

