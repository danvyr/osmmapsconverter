#!/bin/bash

MAPS_BUILD=/home/osm/dev/osmmapsconverter/organicmap/map_build
MAPS_OUT=/var/www/maps/organicmap

chmod 0777 $MAPS_BUILD

DOCKER_IMAGE=9e0bf3776498
#DOCKER_IMAGE=danvyr/organicmap:latest

CONTAINER_NAME=organicmap_mapgenerator_silezian


MAP_URL="http://download.geofabrik.de/europe/poland/dolnoslaskie-latest.osm.pbf"

COUNTRIES="Poland_Lower Silesian Voivodeship"

docker run  -t -i \
--mount type=bind,source=$MAPS_BUILD,target=/organicmaps/maps_build \
--mount type=bind,source=$MAPS_OUT,target=/organicmaps/out \
-e PLANET_URL=$MAP_URL \
-e PLANET_MD5_URL=$MAP_URL".md5" \
-e ORGANICMAP_COUNTRIES="$COUNTRIES" \
-e SUBWAY_URL='https://cdn.organicmaps.app/subway.json' \
-e ORGANICMAP_SKIP='Coastline,MwmStatistics' \
-e THREADS_COUNT=1 \
--name $CONTAINER_NAME $DOCKER_IMAGE
#danvyr/organicmap:latest
#


docker rm $CONTAINER_NAME
