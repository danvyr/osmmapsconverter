#!/bin/sh

#prepare
MKGMAP_VER=latest
SPLITTER_VER=latest

wget http://www.mkgmap.org.uk/download/mkgmap-$MKGMAP_VER.tar.gz

mkdir mkgmap split temp

tar -xf mkgmap-$MKGMAP_VER.tar.gz --directory mkgmap
mv mkgmap/mkgmap-$MKGMAP_VER/* mkgmap
rmdir mkgmap/mkgmap-$MKGMAP_VER
rm mkgmap-$MKGMAP_VER.tar.gz


wget http://www.mkgmap.org.uk/download/splitter-$SPLITTER_VER.tar.gz

tar -xf splitter-$SPLITTER_VER.tar.gz  --directory  split
mv split/splitter-$SPLITTER_VER/* split
rmdir split/splitter-$SPLITTER_VER
rm splitter-$SPLITTER_VER.tar.gz






