#!/bin/bash

set -e

TEMP_DIR=temp
PBF_FILE=$1
PBF_FILE_RU=/var/www/maps/pbf/belarus-ru.osm.pbf
STYLES=styles
BOUNDS=bounds-latest.zip
#MKGMAP=mkgmap
MKGMAP="java -jar mkgmap/mkgmap.jar"
#SPLITTER=mkgmap-splitter
SPLITTER="java -jar split/splitter.jar"
OUT_DIR=out

if [[ -n "$PBF_FILE"  ]]
then
    echo "[INFO] using custom PBF_FILE:"
    echo PBF_FILE=$PBF_FILE
else
    echo "[INFO] using default PBF_FILE:"
    export PBF_FILE=../in/belarus.osm.pbf
    echo PBF_FILE=$PBF_FILE
fi


TEMPLATE_ARGS="$TEMP_DIR/template.args"
STRANGER_STYLE_FILE="$STYLES/my_stranger/"
STRANGER_TYP="$STYLES/my_stranger.typ"
GENERIC_STYLE_FILE="$STYLES/generic_new/"
GENERIC_TYP="$STYLES/generic_new.typ"

DATE=`date +%F`
NAME="Belarus_map"

echo "TEMP_DIR = $TEMP_DIR "
echo "STYLES = $STYLES "
echo "BOUNDS = $BOUNDS "
echo "STRANGER_STYLE_FILE = $STRANGER_STYLE_FILE "
echo "TEMPLATE_ARGS = $TEMPLATE_ARGS "
echo "STRANGER_TYP = $STRANGER_TYP "
echo "DATE = $DATE"
echo "OUT_DIR = $OUT_DIR"

mkdir -p $OUT_DIR

COUNTRY_NAME=Belarus
COUNTRY_CODE=BY

./build_map.sh -i "$PBF_FILE" -o "$OUT_DIR/${NAME}_generic.img" \
	-m "$MKGMAP" -S "$SPLITTER" \
	-f 5050 \
	-n "Belarus OpenStreetMap.by generic" \
	-e "Belarus OpenStreetMap.by generic" \
	-d "OSM default mkgmap style" \
	-c "$COUNTRY_NAME" -k $COUNTRY_CODE

./build_map.sh -i "$PBF_FILE" -o "$OUT_DIR/${NAME}_stranger.img" \
	-m "$MKGMAP" -S "$SPLITTER" \
	-s styles/my_stranger -t styles/my_stranger.typ \
	-f 5052 \
	-n "Belarus OpenStreetMap + ST-GIS by Maks Vasilev" \
	-e "Belarus OpenStreetMap.by velo100" \
	-y "OpenStreetMap CC-BY-SA 2.0, ST-GIS CC-BY-SA 3.0, ST-GIS, Maks Vasilev" \
	-d "Belarus_velo100, v.$DATE" \
	-c "$COUNTRY_NAME" -k $COUNTRY_CODE

./build_map.sh -i "$PBF_FILE" -o "$OUT_DIR/${NAME}_generic_new.img" \
	-m "$MKGMAP" -S "$SPLITTER" \
	-s styles/generic_new -t styles/generic_new.typ \
	-f 5053 \
	-n "Belarus OpenStreetMap generic, new" \
	-e "Belarus OpenStreetMap.by generic, new" \
	-d "Belarus_generic_new, v.$DATE" \
	-c "$COUNTRY_NAME" -k $COUNTRY_CODE


PBF_FILE=$PBF_FILE_RU

./build_map.sh -i "$PBF_FILE" -o "$OUT_DIR/${NAME}_generic_ru.img" \
	-m "$MKGMAP" -S "$SPLITTER" \
	-f 5054 \
	-n "Belarus OpenStreetMap.by generic (ru)" \
	-e "Belarus OpenStreetMap.by generic (ru)" \
	-d "OSM default mkgmap style, ru" \
	-c "$COUNTRY_NAME" -k $COUNTRY_CODE

./build_map.sh -i "$PBF_FILE" -o "$OUT_DIR/${NAME}_stranger_ru.img" \
	-m "$MKGMAP" -S "$SPLITTER" \
	-s styles/my_stranger -t styles/my_stranger.typ \
	-f 5055 \
	-n "Belarus OpenStreetMap + ST-GIS by Maks Vasilev (ru)" \
	-e "Belarus OpenStreetMap.by velo100 (ru)" \
	-y "OpenStreetMap CC-BY-SA 2.0, ST-GIS CC-BY-SA 3.0, ST-GIS, Maks Vasilev" \
	-d "Belarus_velo100, v.$DATE, ru" \
	-c "$COUNTRY_NAME" -k $COUNTRY_CODE

./build_map.sh -i "$PBF_FILE" -o "$OUT_DIR/${NAME}_generic_new_ru.img" \
	-m "$MKGMAP" -S "$SPLITTER" \
	-s styles/generic_new -t styles/generic_new.typ \
	-f 5056 \
	-n "Belarus OpenStreetMap generic, new (ru)" \
	-e "Belarus OpenStreetMap.by generic, new" \
	-d "Belarus_generic_new, v.$DATE, ru" \
	-c "$COUNTRY_NAME" -k $COUNTRY_CODE

