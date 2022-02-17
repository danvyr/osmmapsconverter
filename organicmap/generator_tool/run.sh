



MAPS_BUILD=~/dev/osm
chmod 0777 $MAPS_BUILD

docker rm /organicmap_mapgenerator

docker run  -t -i \
    -e PLANET_URL='http://download.geofabrik.de/europe/belarus-latest.osm.pbf' \
    -e PLANET_MD5_URL='http://download.geofabrik.de/europe/belarus-latest.osm.pbf.md5' \
    -e ORGANICMAP_COUNTRIES='Belarus_Minsk Region' \
    -e ORGANICMAP_SKIP='Coastline,MwmStatistics' \
    --mount type=bind,source=$MAPS_BUILD,target=/organicmaps/maps_build \
    --name organicmap_mapgenerator organicmap_generator:latest


# export ORGANICMAP_SKIP="Coastline,MwmStatistics"
# export ORGANICMAP_COUNTRIES="Belarus*"

# export PLANET_MD5_URL=$PLANET_MD5_URL
# export PLANET_URL=http://download.geofabrik.de/europe/belarus-latest.osm.pbf
# PLANET_MD5_URL=http://download.geofabrik.de/europe/belarus-latest.osm.pbf.md5

# docker run \
#   --name organicmap_mapgenerator \
#   --mount type=bind,source=$MAPS_BUILD,target=/organicmaps/maps_build \
#   organicmap_mapgenerator:master   --config='/home/ubuntu/map_generator.ini'  --skip="Coastline,MwmStatistics" --countries="Belarus_Minsk Region"
