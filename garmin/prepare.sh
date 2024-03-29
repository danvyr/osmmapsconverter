#!/bin/sh

#prepare
MKGMAP_VER=latest
SPLITTER_VER=latest

wget http://www.mkgmap.org.uk/download/mkgmap-$MKGMAP_VER.tar.gz

rm -rf mkgmap split temp
mkdir mkgmap split temp

tar -xf mkgmap-$MKGMAP_VER.tar.gz --directory mkgmap
mv mkgmap/mkgmap-*/* mkgmap
rm -rf mkgmap/mkgmap-*
rm mkgmap-$MKGMAP_VER.tar.gz


wget http://www.mkgmap.org.uk/download/splitter-$SPLITTER_VER.tar.gz

tar -xf splitter-$SPLITTER_VER.tar.gz  --directory  split
mv split/splitter-*/* split
rm -rf  split/splitter-*
rm splitter-$SPLITTER_VER.tar.gz

rm -rf bounds*
curl https://www.thkukuk.de/osm/data/bounds-latest.zip --output bounds-latest.zip
curl https://www.thkukuk.de/osm/data/sea-latest.zip --output sea-latest.zip
