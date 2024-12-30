# This is container for script for change "default language" in PBF files from Belarusian to russian

Script for changing tags: https://github.com/tbicr/osm-name-migrate/blob/main/osm_back.py

Docker file and bash script for container https://github.com/danvyr/osmmapsconverter/tree/master/rus

Volume: PBF_DIR   - folder with files

Options: PBF_FILE PBF_FILE_RU  


Example how it work:
```bash
echo "[INFO] Downloading belarus-latest.osm.pbf from geofabrik.de"
aria2c -s8 -x8  https://download.geofabrik.de/europe/belarus-latest.osm.pbf

echo "[INFO] Start changing language"

IMAGE_NAME="danvyr/osm_back"
CONTAINER_NAME=osm_back
PBF_FILE=belarus-latest.osm.pbf
PBF_FILE_RU=belarus-latest-ru.osm.pbf
PBF_DIR=$(realpath .)

docker run  -e PBF_FILE=$PBF_FILE -e PBF_FILE_RU=$PBF_FILE_RU --mount type=bind,src=$PBF_DIR,dst=/pbf --name $CONTAINER_NAME  $IMAGE_NAME 

docker rm $CONTAINER_NAME
```