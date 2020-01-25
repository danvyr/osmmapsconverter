#!/bin/sh

#prepare
wget http://www.mkgmap.org.uk/download/mkgmap-r4425.tar.gz

mkdir mkgmap
tar -xf mkgmap-r4425.tar.gz --directory mkgmap
mv mkgmap/mkgmap-r4425/* mkgmap
rmdir mkgmap/mkgmap-r4425
rm mkgmap-r4425.tar.gz

#rmdir split

mkdir split temp

wget http://www.mkgmap.org.uk/download/splitter-r595.tar.gz

tar -xf splitter-r595.tar.gz  --directory  split
mv split/splitter-r595/* split
rmdir split/splitter-r595
rm splitter-r595.tar.gz






