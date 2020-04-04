#!/usr/bin/env python3

# TODO формировать json и xml(osm_downloader format) с датой создания файлов и путями скачивания

# TODO доставание полигонов из osm для любой страны (по админ уровню) или использование полигонов mapsme
# TODO сделать тестовую замену name на name:be
# TODO общий in, для разных приложения, с датой скачивания
# TODO раскидать по модулям ?


import logging
import sys
import requests
import urllib.request
import os
import shutil
import datetime
import email.utils as eut
from datetime import datetime, date, time
from multiprocessing import Pool
# from multiprocessing.dummy import Pool as ThreadPool

from multiprocessing import cpu_count

urls = {
    'osmandcreator': 'https://download.osmand.net/latest-night-build/OsmAndMapCreator-main.zip',
    'maps':
        {'belarus': 'http://download.geofabrik.de/europe/belarus-latest.osm.pbf',

         }
}
#mapsme_maps='Belarus_Brest Region Belarus_Homiel Region Belarus_Hrodna Region Belarus_Maglieu Region Belarus_Minsk Region Belarus_Vitebsk Region'
mapsme_maps=['Belarus_Minsk Region',
             'Belarus_Brest Region',
             'Belarus_Homiel Region',
             'Belarus_Hrodna Region',
             'Belarus_Maglieu Region',
             'Belarus_Vitebsk Region']


user = 'osm'
javaOpt = ' -Xms128M -Xmx3200M '

currentDir = os.path.abspath('.')
currentMap = os.path.join(currentDir, 'currentMap.txt')
currentStatus = os.path.join(currentDir, 'status.txt')

inputDir = os.path.abspath('in')

polyDir = os.path.abspath('poly')
splitDir = os.path.abspath('split')
logsDir = os.path.abspath('logs')

mapsmeDir = os.path.abspath('mapsme')
osmandDir = os.path.abspath('osmand')
garminDir = os.path.abspath('garmin')

OAMCDir = os.path.join(osmandDir, 'OsmAndMapCreator')

tempGarmin = os.path.join(garminDir, 'temp')
tempMapsme = os.path.join(mapsmeDir, 'temp')
tempSplit = os.path.join(currentDir, 'split')

# in  mapsme/omim/tools/python/maps_generator/var/etc/map_generator.ini MAIN_OUT_PATH: <full_path>/mapsme/temp

outDir = os.path.join('/var/www/maps')
outOsmAnd = os.path.join(outDir, 'osmand')
outMapsme = os.path.join(outDir, 'mapsme')
outGarmin = os.path.join(outDir, 'garmin')

tempDirs = [inputDir, tempMapsme, tempGarmin, tempSplit]
innerDirs = [polyDir, splitDir, mapsmeDir, osmandDir, garminDir, OAMCDir, logsDir]
outDirs = [outDir, outOsmAnd, outMapsme, outGarmin]

moveCount = 0



logfile = os.path.join(logsDir, 'osmmapcreator_' + str(datetime.today().strftime('%Y-%m-%d_%H-%M-%S')) + '.log')
logging.basicConfig(filename=logfile, level=logging.INFO)


def run_command(command):
    log (command)
    os.system(command)


def nowtime():
    return datetime.today().strftime('%H-%M-%S: ')

def log(status):
    s = nowtime() + status
    print(s)
    logging.info(s)


def readStatus():
    try:
        with open(currentStatus, 'r') as f:
            return  f.readline()
    except:
        with open(currentStatus, 'w') as f:
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
    version = ""
    try:
        with open(currentMap, 'r') as vf:
            version = vf.readline()
            if version != urlDate:
                return 1
            else:
                return 0
    except:
        log ('first launch')
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

    try:
        log('install mapsme')

        os.system('sudo apt-get install git qtbase5-dev cmake libsqlite3-dev clang libc++-dev libboost-iostreams-dev libglu1-mesa-dev python3-pip -y')
        os.chdir(mapsmeDir)
        os.system(
            'git clone --depth=1 --recursive https://github.com/mapsme/omim.git')
        os.chdir(mapsmeDir + '/omim')
        os.system('./configure.sh')
        os.system('./tools/unix/build_omim.sh -sr generator_tool')
        os.chdir('tools/python/maps_generator')
        os.system('pip3 install -r requirements.txt')
        os.system('cp ' + os.path.join(mapsmeDir,
                                       '/map_generator.ini') + ' var/etc/map_generator.ini')
        os.chdir(currentDir)

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


def moveMapsme():

    mapsmeCount = 0
    global moveCount
    log('find mapme maps')
    # find mapme maps
    path = ''
    status = False
    for folder in os.listdir(tempMapsme):
        dirL1 = os.path.join(tempMapsme, folder)
        if (folder.find('20') > -1) and os.path.isdir(dirL1):
            log(dirL1)
            for t in os.listdir(dirL1):
                dirL2 = os.path.join(dirL1, t)
                if (t.find('20') > -1) and os.path.isdir(dirL2):
                    os.chdir(dirL2)
                    with open(os.path.join(dirL1, 'status/stages.status'), 'r') as f:
                        str = f.readline()
                        log(str)
                        if str == 'finish':
                            status = True
                            path = dirL2
                            log(path)
            os.chdir(tempMapsme)

    # moving mapsme maps
    log('move mapsme map')
    if status:
        for file in os.listdir(path):
            if file.endswith('.mwm'):
                logging.info(file)
                shutil.move(os.path.join(path, file),
                            os.path.join(outMapsme, file))
                mapsmeCount = mapsmeCount + 1
    os.chdir(currentDir)

    moveCount = moveCount + mapsmeCount
    return mapsmeCount


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
    # move garmin
    log('move garmin map')
    try:
        shutil.move(os.path.join(tempGarmin, 'gmapsupp_general.img'),
                    os.path.join(outGarmin, 'gmapsupp_general.img'))
        shutil.move(os.path.join(tempGarmin, 'gmapsupp_stranger.img'),
                    os.path.join(outGarmin, 'gmapsupp_stranger.img'))
        shutil.move(os.path.join(tempGarmin, 'gmapsupp_routes_bicycle.img'),
                    os.path.join(outGarmin, 'gmapsupp_routes_bicycle.img'))
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
        for mapFile in os.listdir(inputDir):
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


def mapsme():
    log('Start MAPSME map Creator')
    os.chdir(os.path.join(mapsmeDir, 'omim/tools/python'))
    print (len(mapsme_maps))
    for map in mapsme_maps:
        log('Start ' + str(map))
        os.chdir(os.path.join(mapsmeDir, 'omim/tools/python'))
        os.system('python3.6 -m maps_generator --countries="' + map + '" --skip="coastline"')
        moveMapsme()
        clean()
    os.chdir(currentDir)
    log('Finish MAPSME maps')
 #   moveMapsme()


def garmin():
    log('Start GARMIN map Creator')
    os.chdir(garminDir)
    os.system('bash build.sh')
    os.chdir(currentDir)
    log('Finish GARMIN map Creator')

    moveGarmin()


def main():
 #   prepare():


    log('Started')

    if readStatus() == 'finished':
        writeStatus('running')
        checkDirs()

        dl = checkURL()

        log ('Check version = '+ dl)

        if checkVersion(dl):
            log('Run ')
            if(download()):
                log('downloaded')
                if split():
                    osmand()
                garmin()
            mapsme()
            if(moveCount > 1):
                writeVersion(dl)
                log('Something done')
            else:
                log('Nothing done')

        else:
            log('old map')

        clean()
        writeStatus('finished')

    else:
        log('Can\'t start - check status file')


    log('Finished')


if __name__ == '__main__':
    main()

