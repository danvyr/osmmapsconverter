#!/bin/bash

MAP_GENERATOR_INI=$HOME/organicmaps/tools/python/maps_generator/var/etc/map_generator.ini
MAP_GENERATOR_INI_TEMPLATE=$HOME/map_generator.ini.template

echo "[INFO] ENV:"

echo PLANET_URL=$PLANET_URL
echo PLANET_MD5_URL=$PLANET_MD5_URL
echo ORGANICMAP_COUNTRIES=$ORGANICMAP_COUNTRIES
echo ORGANICMAP_SKIP=$ORGANICMAP_SKIP

if [[ -n "$SUBWAY_URL"  ]]
then
    echo "[INFO] using custom SUBWAY_URL:"
    echo SUBWAY_URL=$SUBWAY_URL
else
    echo "[INFO] using default SUBWAY_URL:"
    export SUBWAY_URL=https://cdn.organicmaps.app/subway.json
    echo SUBWAY_URL=$SUBWAY_URL
fi


echo "[INFO] Change map_generator.ini:"

envsubst < "$MAP_GENERATOR_INI_TEMPLATE" > "$MAP_GENERATOR_INI"

cat $MAP_GENERATOR_INI


echo "[INFO] Start generate"

if [[ -n "$ORGANICMAP_COUNTRIES" && -n  "$ORGANICMAP_SKIP" ]]
then
    python3 -m maps_generator --skip="$ORGANICMAP_SKIP" --countries="$ORGANICMAP_COUNTRIES"
else
    echo "[INFO] Not all parameters"
fi



