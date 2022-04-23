#!/usr/bin/env python3


import sys
import os
import shutil


def moveOrganicmaps(tempOrganicmap, outOrganicmaps):

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
                shutil.move(os.path.join(path, file),
                            os.path.join(outOrganicmaps, file))
    else:
        print('Not move Organicmaps map')


def main():
    tempOrganicmap = os.environ.get('HOME')+"/maps_build"
    outOrganicmaps = os.environ.get('HOME')+"/out"
    print("[INFO] maps_build " + tempOrganicmap)
    print("[INFO] out " + outOrganicmaps)

    moveOrganicmaps(tempOrganicmap, outOrganicmaps)


if __name__ == '__main__':
    main()
