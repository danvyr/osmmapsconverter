#!/bin/bash


CURRENT_DIR=$(pwd)
MAPS_BUILD=$CURRENT_DIR/map_build
MAPS_OUT=$CURRENT_DIR

chmod 0777 $MAPS_BUILD

DOCKER_IMAGE=danvyr/organicmap:latest
CONTAINER_NAME=organicmap_mapgenerator
docker rm  $CONTAINER_NAME


MAP_URL="http://download.geofabrik.de/europe/belarus-latest.osm.pbf"

COUNTRIES="Belarus_Brest*"

docker run  -t -i \
--mount type=bind,source=$MAPS_BUILD,target=/organicmaps/maps_build \
--mount type=bind,source=$MAPS_OUT,target=/organicmaps/out \
-e PLANET_URL=$MAP_URL \
-e PLANET_MD5_URL=$MAP_URL".md5" \
-e ORGANICMAP_COUNTRIES="$COUNTRIES" \
-e SUBWAY_URL='https://cdn.organicmaps.app/subway.json' \
-e ORGANICMAP_SKIP='Coastline,MwmStatistics' \
-e THREADS_COUNT=8 \
--name $CONTAINER_NAME $DOCKER_IMAGE



echo "[INFO] Deleting container docker rm $CONTAINER_NAME"
docker rm $CONTAINER_NAME


