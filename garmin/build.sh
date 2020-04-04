#!/bin/sh

TEMP_DIR=temp
PBF_FILE=../in/belarus-latest.osm.pbf
# PBF_FILE=~/belarus-latest-internal.osm.pbf
STYLES=styles
BOUNDS=bounds

STYLE_FILE="$STYLES/my_stranger/"
TEMPLATE_ARGS="$TEMP_DIR/template.args"
TYP="$STYLES/my_stranger.typ"

echo "TEMP_DIR = $TEMP_DIR "
echo "STYLES = $STYLES "
echo "BOUNDS = $BOUNDS "
echo "STYLE_FILE = $STYLE_FILE "
echo "TEMPLATE_ARGS = $TEMPLATE_ARGS "
echo "TYP = $TYP "


java -jar split/splitter.jar \
    --max-nodes=1200000 \
    --overlap=12000 \
    --keep-complete=false \
    --output=pbf \
    --output-dir=$TEMP_DIR \
    $PBF_FILE

java -jar mkgmap/mkgmap.jar \
    --route --add-pois-to-areas \
    --bounds=bounds --index  \
    --gmapsupp --mapname=80808080 \
    --link-pois-to-ways \
    --country-name=Belarus \
    --country-abbr=BY  \
    "temp\6324*.osm.pbf"

mv $TEMP_DIR/gmapsupp.img $TEMP_DIR/gmapsupp_general.img


java -jar mkgmap/mkgmap.jar \
    --route --add-pois-to-areas \
    --bounds=bounds --index  \
    --gmapsupp --mapname=80808081 \
    --link-pois-to-ways \
    --style=routes-bicycle \
    --country-name=Belarus \
    --country-abbr=BY  \
    "temp\6324*.osm.pbf"

mv $TEMP_DIR/gmapsupp.img $TEMP_DIR/gmapsupp_routes_bicycle.img


java -jar mkgmap/mkgmap.jar \
    --verbose \
    --output-dir=$TEMP_DIR \
    --gmapsupp \
    --tdbfile \
    --family-name="OpenStreetMap + ST-GIS by Maks Vasilev" \
    --product-id=1 \
    --family-id=43 \
    --description="velo100, v.%DATE%" \
    --country-name="BELARUS" \
    --country-abbr="BY" \
    --copyright-message="OpenStreetMap CC-BY-SA 2.0, ST-GIS CC-BY-SA 3.0, ST-GIS, Maks Vasilev" \
    --charset=cp1251 \
    --code-page=1251 \
    --lower-case \
    --name-tag-list=name,name:ru,name:be,int_name \
    --style-file=$STYLE_FILE \
    --remove-short-arcs \
    --drive-on=right \
    --check-roundabouts \
    --mapname=80808082 \
    --make-poi-index \
    --index \
    --poi-address \
    --route \
    --draw-priority=31 \
    --bounds=$BOUNDS \
    --housenumbers \
    --add-pois-to-areas \
    -c $TEMPLATE_ARGS  $TYP



mv $TEMP_DIR/gmapsupp.img $TEMP_DIR/gmapsupp_stranger.img

