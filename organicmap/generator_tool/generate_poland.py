#!/usr/bin/env python3


import os
import logging
import shutil


import logging
import sys
import requests
import urllib.request
import os
import shutil
import glob
import datetime
import email.utils as eut
from datetime import datetime, date, time
from multiprocessing import Pool
# from multiprocessing.dummy import Pool as ThreadPool

from multiprocessing import cpu_count

poland = [
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

currentDir = os.path.abspath('/home/osm/dev/osmmapsconverter/')
currentMap = os.path.join(currentDir, 'currentMap.txt')
currentStatus = os.path.join(currentDir, 'status.txt')
MAPS_BUILD_DEF = "/home/osm/dev/osmmapsconverter/organicmap/map_build"


organicmapDir = os.path.abspath('organicmap')

tempOrganicmap = os.path.join(organicmapDir, 'map_build')

# in  organicmap/omim/tools/python/maps_generator/var/etc/map_generator.ini MAIN_OUT_PATH: <full_path>/organicmap/temp

outDir = os.path.join('/var/www/maps')
outOrganicmaps = os.path.join(outDir, 'organicmap')

tempDirs = [tempOrganicmap]
innerDirs = [organicmapDir]
outDirs = [outOrganicmaps]
logsDir = os.path.abspath('logs')

logfile = os.path.join(logsDir, 'organic_' + str(datetime.today().strftime('%Y-%m-%d_%H-%M-%S')) + '.log')
logging.basicConfig(filename=logfile, level=logging.INFO)

def run_command(command):
    print("RUN COMAND")
    os.system("docker rm "+ command[2])
    print (command[0])
    logging.info(str(command))
    os.system(command[0])
    clean(command[1])
    os.system("docker rm "+ command[2])


def log(status):
    s = nowtime() + status
    print(s)
    logging.info(s)

def clean(folder):
    print('Clean folders:')


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

    file_path = os.path.join(currentDir, filename)
    try:
        if (os.path.isfile(file_path) or os.path.islink(file_path)) and filename.find('osmconvert_tempfile') > -1:
            os.unlink(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))



def generate():
    print("gen")
    cmd_rm = "docker rm /organicmap_mapgenerator "

    pool = Pool(cpu_count())
    try:
        cmds = []
        i=0
        for map_name, map_url in poland:
#            clean()
            try:
                pass
                #os.system(cmd_rm)
            except:
                pass

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
            "-e THREADS_COUNT=1 "+ \
            "--name " + CONTAINER_NAME + " danvyr/organicmap:latest"

            cmds.append([cmd, MAPS_BUILD, CONTAINER_NAME])
            i+=1

        logging.info(str(cmds))

        print (cmds)
        print ("START")
        pool.map(run_command, cmds)
        pool.close()
        pool.join()

    except:
        pass

def moveOrganicmaps():

    organicmapsCount = 0
    print('find mapme maps')
    # find mapme maps
    path = ''
    status = False
    for folder in os.listdir(tempOrganicmap):
        dirL1 = os.path.join(tempOrganicmap, folder)
        if (folder.find('20') > -1) and os.path.isdir(dirL1):
            print(dirL1)
            t = folder[2:10].replace('_', '')
            print(t)
            dirL2 = os.path.join(dirL1, t)
            print(dirL2)
            if os.path.isdir(dirL2):
                os.chdir(dirL2)
                print(dirL2)
                status_file = os.path.join(dirL1, 'status/stages.status')
                print(status_file)
                with open(status_file, 'r') as f:
                    str = f.readline()
                    print('Status ')
                    print(str)
                    if str == 'finish':
                        status = True
                        path = dirL2
                        print(path)
            os.chdir(tempOrganicmap)

    # moving Organicmaps maps
    if status:
        print('move Organicmaps map')
        for file in os.listdir(path):
            if file.endswith('.mwm'):
                logging.info(file)
                shutil.move(os.path.join(path, file),
                            os.path.join(outOrganicmaps, file))
                organicmapsCount = organicmapsCount + 1
    else:
        print('Not move Organicmaps map')
    os.chdir(currentDir)

    return organicmapsCount


def main():
    clean(MAPS_BUILD_DEF)
    generate()
#    moveOrganicmaps()

if __name__ == '__main__':
    main()

