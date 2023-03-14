#!/bin/bash

MAPS_BUILD=~/dev/osmmapsconverter/organicmap/map_build
MAPS_OUT=~/dev/osmmapsconverter/organicmap

chmod 0777 $MAPS_BUILD

# DOCKER_IMAGE=9e0bf3776498
DOCKER_IMAGE=danvyr/organicmap:latest

CONTAINER_NAME=organicmap_mapgenerator_silezian
docker rm  $CONTAINER_NAME

MAP_URL="http://172.17.0.1/belarus-latest.osm.pbf"

COUNTRIES="Belarus*"
COUNTRIES="Belarus_Brest*"
# docker run  -t -i \
# --mount type=bind,source=$MAPS_BUILD,target=/organicmaps/maps_build \
# --mount type=bind,source=$MAPS_OUT,target=/organicmaps/out \
# -e PLANET_URL=$MAP_URL \
# -e PLANET_MD5_URL=$MAP_URL".md5" \
# -e ORGANICMAP_COUNTRIES="$COUNTRIES" \
# -e SUBWAY_URL='https://cdn.organicmaps.app/subway.json' \
# -e ORGANICMAP_SKIP='Coastline,MwmStatistics' \
# -e THREADS_COUNT=8 \
# --name $CONTAINER_NAME $DOCKER_IMAGE

docker run  -t -i \
--mount type=bind,source=$MAPS_BUILD,target=/organicmaps/maps_build \
--mount type=bind,source=$MAPS_OUT,target=/organicmaps/out \
-e PLANET_URL=$MAP_URL \
-e PLANET_MD5_URL=$MAP_URL".md5" \
-e ORGANICMAP_COUNTRIES="$COUNTRIES" \
-e SUBWAY_URL='http://172.17.0.1/subway.json' \
-e ORGANICMAP_SKIP='Coastline,MwmStatistics' \
-e THREADS_COUNT=8 \
--name $CONTAINER_NAME $DOCKER_IMAGE




# docker rm $CONTAINER_NAME


# http://127.0.0.1/subway.json

# http://127.0.0.1/belarus-latest.osm.pbf
