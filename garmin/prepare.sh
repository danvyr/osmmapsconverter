#!/bin/sh

#prepare
MKGMAP_VER=latest
SPLITTER_VER=latest

wget http://www.mkgmap.org.uk/download/mkgmap-$MKGMAP_VER.tar.gz

mkdir mkgmap split temp

tar -xf mkgmap-$MKGMAP_VER.tar.gz --directory mkgmap
mv mkgmap/mkgmap-*/* mkgmap
rmdir mkgmap/mkgmap-*
rm mkgmap-$MKGMAP_VER.tar.gz


wget http://www.mkgmap.org.uk/download/splitter-$SPLITTER_VER.tar.gz

tar -xf splitter-$SPLITTER_VER.tar.gz  --directory  split
mv split/splitter-*/* split
rmdir split/splitter-*
rm splitter-$SPLITTER_VER.tar.gz






