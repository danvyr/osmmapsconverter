#!/usr/bin/env python3


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

# "Ukraine_Cherkasy Oblast",
# "Ukraine_Chernihiv Oblast",
# "Ukraine_Chernivtsi Oblast",
# "Ukraine_Dnipropetrovsk Oblast",
# "Ukraine_Donetsk Oblast",
# "Ukraine_Ivano-Frankivsk Oblast",
# "Ukraine_Kharkiv Oblast",
# "Ukraine_Kherson Oblast",
# "Ukraine_Khmelnytskyi Oblast",
# "Ukraine_Kirovohrad Oblast",
# "Ukraine_Kyiv Oblast",
# "Ukraine_Luhansk Oblast",
# "Ukraine_Lviv Oblast",
# "Ukraine_Mykolaiv Oblast",
# "Ukraine_Odessa Oblast",
# "Ukraine_Poltava Oblast",
# "Ukraine_Rivne Oblast",
# "Ukraine_Sumy Oblast",
# "Ukraine_Ternopil Oblast",
# "Ukraine_Vinnytsia Oblast",
# "Ukraine_Volyn Oblast",
# "Ukraine_Zakarpattia Oblast",
# "Ukraine_Zaporizhia Oblast",
# "Ukraine_Zhytomyr Oblast",


ukraine = [

    ["Ukraine_Lviv Oblast",
     "http://download.geofabrik.de/europe/ukraine-latest.osm.pbf"],

]

currentDir = os.path.abspath('//home/vitali/dev/osmmapsconverter')
currentMap = os.path.join(currentDir, 'currentMap.txt')
currentStatus = os.path.join(currentDir, 'status.txt')


organicmapDir = os.path.abspath('organicmap')

tempOrganicmap = os.path.abspath('/home/vitali/dev/osm/')

# in  organicmap/omim/tools/python/maps_generator/var/etc/map_generator.ini MAIN_OUT_PATH: <full_path>/organicmap/temp

outDir = os.path.join('/var/www/maps')
outOrganicmaps = os.path.join(outDir, 'organicmap')

tempDirs = [tempOrganicmap]
innerDirs = [organicmapDir]
outDirs = [outOrganicmaps]


def clean():
    print('Clean folders:')
    print(str(tempDirs))

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

    # osmconvert_tempfile
    for filename in os.listdir(currentDir):
        file_path = os.path.join(currentDir, filename)
        try:
            if (os.path.isfile(file_path) or os.path.islink(file_path)) and filename.find('osmconvert_tempfile') > -1:
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def generate():

    pool = Pool(cpu_count())

    print("gen")
    cmd_rm = "docker rm /organicmap_mapgenerator "

    MAPS_BUILD = tempOrganicmap
    try:
        cmds = []
        for map_name, map_url in ukraine:
            clean()
            try:
                os.system(cmd_rm)
            except:
                pass

            print(map_name + " " + map_url)

            cmd = "docker run  -t -i \
            --mount type=bind,source=" + MAPS_BUILD + ",target=/organicmaps/maps_build \
            -e PLANET_URL='" + map_url + "' \
            -e PLANET_MD5_URL='" + map_url + ".md5' \
            -e ORGANICMAP_COUNTRIES='" + map_name + "' \
            -e ORGANICMAP_SKIP='Coastline,MwmStatistics' \
            --name organicmap_mapgenerator danvyr/organicmap:latest"
            print(cmd)
            cmds.append(cmd)

        pool.map(os.system(cmds), cmds)
        pool.close()
        pool.join()

        moveOrganicmaps()
    except:
        pass


def moveOrganicmaps():

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
    else:
        print('Not move Organicmaps map')
    os.chdir(currentDir)


def main():
    generate()


if __name__ == '__main__':
    main()
