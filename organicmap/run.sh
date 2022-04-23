#!/bin/bash

MAPS_BUILD=~/dev/osm
chmod 0777 $MAPS_BUILD

docker rm /organicmap_mapgenerator

FILE=https://download.openstreetmap.by/belarus-latest.osm.pbf

docker run  -t -i \
    -e PLANET_URL="$FILE" \
    -e PLANET_MD5_URL="$FILE.md5" \
    -e ORGANICMAP_COUNTRIES='Belarus*' \
    -e ORGANICMAP_SKIP='Coastline,MwmStatistics' \
    -e SUBWAY_URL='https://cdn.organicmaps.app/subway.json' \
    --mount type=bind,source=$MAPS_BUILD,target=/organicmaps/maps_build \
    --mount type=bind,source=$MAPS_BUILD,target=/organicmaps/out \
    --name organicmap_mapgenerator danvyr/organicmap:latest
