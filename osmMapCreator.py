#!/usr/bin/python3.6

# TODO сделать автоперезапуск, если файл на geofabric ещё старый (нужен статус файл и его проверка, что бы был только один скрипт запущен)
# TODO формировать json и xml(osm_downloader format) с датой создания файлов и путями скачивания

# TODO доставание полигонов из osm для любой страны (по админ уровню) или использование полигонов mapsme
# TODO сделать тестовую замену name на name:be
# TODO общий in, для разных приложения, с датой скачивания
# TODO раскидать по модулям ?


import sys
import requests
import urllib.request
import os
import shutil
import datetime
import email.utils as eut

from multiprocessing import Pool
# from multiprocessing.dummy import Pool as ThreadPool

from multiprocessing import cpu_count

urls = {
    'osmandcreator': 'https://download.osmand.net/latest-night-build/OsmAndMapCreator-main.zip',
    'maps':
        {'belarus': 'http://download.geofabrik.de/europe/belarus-latest.osm.pbf',

         }
}

user = 'osm'

currentDir = os.path.abspath('.')
currentMap = os.path.join(currentDir, 'currentMap.txt')

inputDir = os.path.abspath('in')

polyDir = os.path.abspath('poly')
splitDir = os.path.abspath('split')

mapsmeDir = os.path.abspath('mapsme')
osmandDir = os.path.abspath('osmand')
garminDir = os.path.abspath('garmin')

OAMCDir = osmandDir + '/OsmAndMapCreator'

tempGarmin = os.path.join(garminDir, 'temp')
tempMapsme = os.path.join(mapsmeDir, 'temp')
tempSplit = os.path.join(currentDir, 'split')

# in  mapsme/omim/tools/python/maps_generator/var/etc/map_generator.ini MAIN_OUT_PATH: <full_path>/mapsme/temp

outDir = os.path.abspath('/var/www/maps')
outOsmAnd = outDir + '/osmand'
outMapsme = outDir + '/mapsme'
outGarmin = outDir + '/garmin'

tempDirs = [inputDir, tempMapsme, tempGarmin, tempSplit]

innerDirs = [polyDir, splitDir, mapsmeDir, osmandDir,
             garminDir, OAMCDir]
outDirs = [outDir, outOsmAnd, outMapsme, outGarmin]

moveCount = 0


def run_command(command):
    print (command)
    os.system(command)


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
        print ('first launch')
        return 1


def writeVersion(urlDate):
    try:
        with open(currentMap, 'w') as vf:
            vf.write(urlDate)
    except:
        print('can\'t write version file')


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

    # install
    try:
        print('install osmctools')
        os.system('sudo apt-get install osmctools')
    except:
        pass

    try:
        print('install mapsme')

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
        print('install osmandMapCreator')

        url = urls['osmandcreator']
        resp = requests.head(url)
        print("Last modified: " + resp.headers['last-modified'])
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
    print ('Clean folders:')
    print(tempDirs)
    for folder in tempDirs:
        print(folder)
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if (os.path.isfile(file_path) or os.path.islink(file_path)) and filename != '.gitignore':
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    #osmconvert_tempfile
    for filename in os.listdir(currentDir):
        file_path = os.path.join(currentDir, filename)
        try:
            if (os.path.isfile(file_path) or os.path.islink(file_path)) and filename.find('osmconvert_tempfile') > -1:
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def moveMapsme():

    mapsmeCount = 0

    # find mapme maps
    path = ''
    status = False
    for folder in os.listdir(tempMapsme):
        dirL1 = os.path.join(tempMapsme, folder)
        if (folder.find('20') > -1) and os.path.isdir(dirL1):
            print(dirL1)
            for t in os.listdir(dirL1):
                dirL2 = os.path.join(dirL1, t)
                if (t.find('20') > -1) and os.path.isdir(dirL2):
                    os.chdir(dirL2)
                    with open(os.path.join(dirL1, 'status/stages.status'), 'r') as f:
                        str = f.readline()
                        print(str)
                        if str == 'finish':
                            status = True
                            path = dirL2
                            print(path)
            os.chdir(tempMapsme)

    # moving mapsme maps
    print('move mapsme map')
    if status:
        for file in os.listdir(path):
            if file.endswith('.mwm'):
                print(file)
                shutil.move(os.path.join(path, file),
                            os.path.join(outMapsme, file))
                mapsmeCount = mapsmeCount + 1
    os.chdir(currentDir)
    
    moveCount = moveCount + mapsmeCount
    return mapsmeCount


def moveOsmand():
    osmandCount = 0    
    # move OsmAnd maps
    print('move OsmAND map')
    for file in os.listdir(osmandDir):
        if file.endswith('.obf'):
            print(file)
            shutil.move(os.path.join(osmandDir, file),
                        os.path.join(outOsmAnd, file))
            osmandCount = osmandCount + 1
    moveCount = moveCount + osmandCount
    return osmandCount


def moveGarmin():        
    garminCount = 0
    # move garmin
    print('move garmin map')
    try:
        shutil.move(os.path.join(tempGarmin, 'gmapsupp.img'),
                    os.path.join(outGarmin, 'gmapsupp.img'))
        garminCount = garminCount + 1
    except:
        print('no garmin map')

    moveCount = moveCount + garminCount
    return garminCount


def checkURL():

    print('Cheking maps urls')

    try:
        for map_name, url_to_map in urls['maps'].items():
            print(map_name)
            resp = requests.head(url_to_map)
            urlLastModified = resp.headers['last-modified']
            print (urlLastModified)
            urlRawDate = eut.parsedate(urlLastModified)
            print(urlRawDate)
            urlDate  =  datetime.datetime(*urlRawDate[:6])
            print("Last modified: " + str(urlDate))
            return str(urlDate.isoformat())

    except:
        print('Cheking failed')
        print("Unexpected error:", sys.exc_info()[0])

        return 0


def download():

    print('Start downloading maps')

    try:
        for map_name, url_to_map in urls['maps'].items():
            print(map_name)
            pathToFile = os.path.join(inputDir, map_name + '.osm.pbf')
            print(pathToFile)
            if urllib.request.urlretrieve(url_to_map,  pathToFile):
                print('all downloaded')
                return 1
            else:
               return 0

    except:
        print('downloading failed')
        print("Unexpected error:", sys.exc_info()[0])
        return 0


def split():
    pool = Pool(cpu_count())

    print('start split')
    try:
        cmds = []
        for mapFile in os.listdir(inputDir):
            print(mapFile)
            for polyFile in os.listdir(polyDir):
                print(polyFile)
                cmd = 'osmconvert ' + os.path.join(inputDir, mapFile) + ' -B=' + '"' + os.path.join(polyDir, polyFile) + '"' \
                    + ' --complete-ways --complex-ways -o='  \
                    + '"' + os.path.join(splitDir, polyFile.replace('poly', 'pbf')) + '"'   \
                    + ' --statistics'
                cmds.append(cmd)

        pool.map(run_command, cmds)
        pool.close()
        pool.join()
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
            mapFile = os.path.join(splitDir, mapFile)
            print(mapFile)

            cmd = 'java -Djava.util.logging.config.file="'+OAMCDir+'/logging.properties" \
                -Xms128M -Xmx3000M \
                -cp "'+OAMCDir+'/OsmAndMapCreator.jar:'+OAMCDir+'/lib/*.jar" net.osmand.MainUtilities generate-obf ' \
                + '"' + mapFile + '"'
            print(cmd)
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
    moveOsmand()


def mapsme():
    os.chdir(os.path.join(mapsmeDir, 'omim/tools/python'))
    os.system(
        'python3.6 -m maps_generator --countries="Belarus*" --skip="coastline"')
    os.chdir(currentDir)
    moveMapsme()


def garmin():
    os.chdir(garminDir)
    os.system('bash build.sh')
    os.chdir(currentDir)
    moveGarmin()


def main():
 #   prepare():
    checkDirs()
    dl = checkURL()

    if checkVersion(dl):
        if(download())
            if split():
                osmand()                
            garmin()
            mapsme()
            if(moveCount > 1):
                writeVersion(dl)
    clean()


if __name__ == '__main__':
    main()
