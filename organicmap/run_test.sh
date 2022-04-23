#!/bin/bash

MAPS_BUILD=~/dev/osm
chmod 0777 $MAPS_BUILD



CONTAINER_NAME=organicmap_mapgenerator_bel


MAP_URL="http://download.geofabrik.de/europe/poland/zachodniopomorskie-latest.osm.pbf"

COUNTRIES="Poland_West Pomeranian Voivodeship"

docker run  -t -i \
--mount type=bind,source=$MAPS_BUILD,target=/organicmaps/maps_build \
-e PLANET_URL=$MAP_URL \
-e PLANET_MD5_URL=$MAP_URL".md5" \
-e ORGANICMAP_COUNTRIES="$COUNTRIES" \
-e ORGANICMAP_SKIP='Coastline,MwmStatistics' \
-e THREADS_COUNT=4 \
--name $CONTAINER_NAME danvyr/organicmap:latest

