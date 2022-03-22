#!/bin/bash

MAPS_BUILD=~/dev/osm
chmod 0777 $MAPS_BUILD

docker rm /organicmap_mapgenerator

docker run  -t -i \
    -e PLANET_URL='http://download.geofabrik.de/europe/belarus-latest.osm.pbf' \
    -e PLANET_MD5_URL='http://download.geofabrik.de/europe/belarus-latest.osm.pbf.md5' \
    -e ORGANICMAP_COUNTRIES='Belarus_Minsk Region' \
    -e ORGANICMAP_SKIP='Coastline,MwmStatistics' \
    -e SUBWAY_URL='https://cdn.organicmaps.app/subway.json' \
    --mount type=bind,source=$MAPS_BUILD,target=/organicmaps/maps_build \
    --name organicmap_mapgenerator danvyr/organicmap:latest
