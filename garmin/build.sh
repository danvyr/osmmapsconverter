#!/bin/sh

TEMP_DIR=temp
PBF_FILE=../in/belarus-latest.osm.pbf
# PBF_FILE=~/belarus-latest-internal.osm.pbf
STYLES=styles
BOUNDS=bounds-latest.zip

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

# java -jar split/splitter.jar \
#     --max-nodes=1200000 \
#     --overlap=12000 \
#     --keep-complete=false \
#     --output=pbf \
#     --output-dir=$TEMP_DIR \
#     $PBF_FILE



COUNTRY_NAME=Belarus
COUNTRY_ABBR=BY

FAMILY_ID=5050
MAPNAME=80808080
PRODUCT_ID=1

java -jar mkgmap/mkgmap.jar \
    --route --add-pois-to-areas \
    --index  \
    --bounds=$BOUNDS \
    --gmapsupp \
    --mapname=$MAPNAME \
    --family-id=$FAMILY_ID \
    --product-id=$PRODUCT_ID \
    --series-name="OpenStreetMap.by" \
    --family-name="OpenStreetMap.by" \
    --link-pois-to-ways \
    --country-name=$COUNTRY_NAME \
    --country-abbr=$COUNTRY_ABBR  \
    --description="Belarus_general, v.$DATE" \
    --output-dir=$TEMP_DIR \
    -c $TEMPLATE_ARGS

mv $TEMP_DIR/gmapsupp.img $TEMP_DIR/"$NAME"_general.img


FAMILY_ID=5051
MAPNAME=80808081
PRODUCT_ID=2

java -jar mkgmap/mkgmap.jar \
    --verbose \
    --output-dir=$TEMP_DIR \
    --gmapsupp \
    --tdbfile \
    --series-name="OpenStreetMap.by" \
    --family-name="OpenStreetMap.by" \
    --description="Belarus_routes-bicycle, v.$DATE" \
    --country-name=$COUNTRY_NAME \
    --country-abbr=$COUNTRY_ABBR \
    --charset=cp1251 \
    --code-page=1251 \
    --lower-case \
    --name-tag-list=name,name:ru,name:be,int_name \
    --style=routes-bicycle \
    --remove-short-arcs \
    --drive-on=right \
    --check-roundabouts \
    --mapname=$MAPNAME \
    --family-id=$FAMILY_ID \
    --product-id=$PRODUCT_ID \
    --make-poi-index \
    --index \
    --poi-address \
    --route \
    --draw-priority=31 \
    --bounds=$BOUNDS \
    --housenumbers \
    --add-pois-to-areas \
    -c $TEMPLATE_ARGS  $GENERIC_TYP
    
# java -jar mkgmap/mkgmap.jar \
#     --route --add-pois-to-areas \
#     --bounds=$BOUNDS \
#     --index  \
#     --gmapsupp \
#     --mapname=$MAPNAME \
#     --family-id=$FAMILY_ID \
#     --link-pois-to-ways \
#     --style=routes-bicycle \
#     --country-name=$COUNTRY_NAME \
#     --country-abbr=$COUNTRY_ABBR  \
#     --description="Belarus_bicycle, v.$DATE" \
#     --output-dir=$TEMP_DIR \
#     -c $TEMPLATE_ARGS

mv $TEMP_DIR/gmapsupp.img $TEMP_DIR/"$NAME"_routes_bicycle.img


FAMILY_ID=5052
MAPNAME=80808082
PRODUCT_ID=3

java -jar mkgmap/mkgmap.jar \
    --verbose \
    --output-dir=$TEMP_DIR \
    --gmapsupp \
    --tdbfile \
    --series-name="OpenStreetMap.by" \
    --family-name="OpenStreetMap.by" \
    --family-name="OpenStreetMap + ST-GIS by Maks Vasilev" \
    --description="Belarus_velo100, v.$DATE" \
    --country-name=$COUNTRY_NAME \
    --country-abbr=$COUNTRY_ABBR \
    --copyright-message="OpenStreetMap CC-BY-SA 2.0, ST-GIS CC-BY-SA 3.0, ST-GIS, Maks Vasilev" \
    --charset=cp1251 \
    --code-page=1251 \
    --lower-case \
    --name-tag-list=name,name:ru,name:be,int_name \
    --style-file=$STRANGER_STYLE_FILE \
    --remove-short-arcs \
    --drive-on=right \
    --check-roundabouts \
    --mapname=$MAPNAME \
    --family-id=$FAMILY_ID \
    --product-id=$PRODUCT_ID \
    --make-poi-index \
    --index \
    --poi-address \
    --route \
    --draw-priority=31 \
    --bounds=$BOUNDS \
    --housenumbers \
    --add-pois-to-areas \
    -c $TEMPLATE_ARGS  $STRANGER_TYP
mv $TEMP_DIR/gmapsupp.img $TEMP_DIR/"$NAME"_stranger.img


FAMILY_ID=5053
MAPNAME=80808083
PRODUCT_ID=4

java -jar mkgmap/mkgmap.jar \
    --verbose \
    --output-dir=$TEMP_DIR \
    --gmapsupp \
    --tdbfile \
    --series-name="OpenStreetMap.by" \
    --family-name="OpenStreetMap.by" \
    --description="Belarus_generic_new, v.$DATE" \
    --country-name=$COUNTRY_NAME \
    --country-abbr=$COUNTRY_ABBR \
    --charset=cp1251 \
    --code-page=1251 \
    --lower-case \
    --name-tag-list=name,name:ru,name:be,int_name \
    --style-file=$GENERIC_STYLE_FILE \
    --remove-short-arcs \
    --drive-on=right \
    --check-roundabouts \
    --mapname=$MAPNAME \
    --family-id=$FAMILY_ID \
    --product-id=$PRODUCT_ID \
    --make-poi-index \
    --index \
    --poi-address \
    --route \
    --draw-priority=31 \
    --bounds=$BOUNDS \
    --housenumbers \
    --add-pois-to-areas \
    -c $TEMPLATE_ARGS  $GENERIC_TYP


mv $TEMP_DIR/gmapsupp.img $TEMP_DIR/"$NAME"_generic_new.img
