MAPS_BUILD=/home/osm/dev/osmmapsconverter/organicmap/map_build

chmod 0777 $MAPS_BUILD

docker rm /organicmap_mapgenerator

docker run \
  --name organicmap_mapgenerator \
  --mount type=bind,source=$MAPS_BUILD,target=/organicmaps/maps_build \
  organicmap:latest  \
   --skip="Coastline,MwmStatistics" --countries="Belarus*"

